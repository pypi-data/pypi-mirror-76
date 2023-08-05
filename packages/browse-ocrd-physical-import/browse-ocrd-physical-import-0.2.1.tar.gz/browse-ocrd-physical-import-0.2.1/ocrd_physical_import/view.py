import cv2
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf
from ocrd_models import OcrdFile
from pkg_resources import resource_filename
from typing import List, Any, Optional
from voussoir.pagewarper import PageWarper, LayoutInfo
from numpy import array as ndarray

from .scandriver import DummyDriver, AndroidADBDriver, AbstractScanDriver
from ocrd_browser.util.image import cv_scale, cv_to_pixbuf
from ocrd_browser.view import View
from ocrd_browser.model import DEFAULT_FILE_GROUP


class ViewScan(View):
    """
    Imports book pages from reality
    """

    label = 'Scan'

    def __init__(self, name: str, window: Gtk.Window):
        super().__init__(name, window)
        # self.driver = AndroidADBDriver()
        self.driver: AbstractScanDriver = DummyDriver('/home/jk/Projekte/archive-tools/projects/exit1/orig/')
        self.driver.setup()

        self.ui: ScanUi = None
        self.previews: List[GdkPixbuf.Pixbuf] = []
        self.layouts: List[LayoutInfo] = []
        self.images: List[ndarray] = []
        # TODO: Braucht man das noch?
        self.selected_page_ids: List[str] = []

    def build(self) -> None:
        super().build()
        self.ui = ScanUi(self, parent=self.viewport)
        self.previews = [self.ui.preview_left, self.ui.preview_right]
        self.window.actions.create('scan', self.on_scan)
        self.window.actions.create('append', self.on_append)
        self.window.actions.create('insert', self.on_insert)
        self.update_ui()

    def on_scan(self, _action: Gio.SimpleAction, _param: Optional[str]) -> None:
        pw = PageWarper()
        try:
            file = str(self.driver.scan())
            image = cv2.imread(file)
            pw.set_image(image)
        except Exception as err:
            print(err)
            raise err

        if not self.layouts:
            self.layouts = pw.guess_layouts(0.1, 0.65, 0.5, -0.15, 300)

        try:
            self.images = []
            for n, layout in enumerate(self.layouts):
                self.images.append(pw.get_warped_image(layout, n == 1))
        except Exception as err:
            print('Warp: ' + str(err))
        self.redraw()

    def on_append(self, _action: Gio.SimpleAction, _param: Optional[str]) -> None:
        for image in self.images:
            self._add_image(image)

        self.document.save()
        self.images = []
        self.update_ui()

    def on_insert(self, _action: Gio.SimpleAction, _param: Optional[str]) -> None:
        page_ids = self.document.page_ids
        inserted_page_ids = []
        for image in self.images:
            inserted_page_ids.append(self._add_image(image).pageId)

        if len(page_ids):
            index = page_ids.index(self.page_id)
            new_page_order = page_ids[:index] + inserted_page_ids + page_ids[index:]
            self.document.reorder(new_page_order)

        self.document.save()
        self.images = []
        self.update_ui()

    def _add_image(self, image:ndarray) -> OcrdFile:
        file_group = DEFAULT_FILE_GROUP
        template_page_id = 'PAGE_{page_nr:04d}'
        template_file_id = '{file_group}_{page_nr:04d}'
        page_id, page_nr = self.document.get_unused_page_id(template_page_id)
        file_id = template_file_id.format(**{'page_nr': page_nr, 'file_group': file_group})
        return self.document.add_image(image, page_id, file_id)

    def pages_selected(self, _sender: Gtk.Widget, page_ids: List[str]) -> None:
        self.selected_page_ids = page_ids
        self.update_ui()

    def update_ui(self) -> None:
        self.window.actions['insert'].set_enabled(self.images and self.page_id)
        self.window.actions['append'].set_enabled(self.images)

    @property
    def use_file_group(self) -> str:
        return 'OCR-D-IMG'

    def config_changed(self, name: str, value: Any) -> None:
        super().config_changed(name, value)
        self.reload()

    def redraw(self) -> None:
        self.update_ui()
        if self.images:
            for image, preview in zip(self.images, self.previews):
                scaled = cv_scale(image, None, self.ui.preview_height)
                preview.set_from_pixbuf(cv_to_pixbuf(scaled))


@Gtk.Template(filename=resource_filename(__name__, 'scan.ui'))
class ScanUi(Gtk.Box):
    __gtype_name__ = 'ScanUi'

    preview_left: Gtk.Image = Gtk.Template.Child()
    preview_right: Gtk.Image = Gtk.Template.Child()

    def __init__(self, view: ViewScan, **kwargs: Any):
        Gtk.Box.__init__(self, **kwargs)
        self.view: ViewScan = view
        self.preview_height: int = 10

    @Gtk.Template.Callback()
    def on_size_allocate(self, sender: Gtk.Widget, rect: Gdk.Rectangle) -> None:
        if abs(self.preview_height - rect.height) > 4:
            self.preview_height = rect.height
            self.view.redraw()
