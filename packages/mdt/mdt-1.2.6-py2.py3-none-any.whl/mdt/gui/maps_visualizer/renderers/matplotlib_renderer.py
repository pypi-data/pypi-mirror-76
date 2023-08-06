import logging
import matplotlib
import numpy as np
import copy
from mdt.gui.maps_visualizer.actions import SetZoom, SetAnnotations

matplotlib.use('Qt5Agg')

from PyQt5.QtCore import QTimer

from mdt.visualization.maps.matplotlib_renderer import MapsVisualizer
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from mdt.gui.maps_visualizer.base import DataConfigModel
from mdt.gui.maps_visualizer.renderers.base import PlottingFrame
from mdt.visualization.maps.base import Zoom, VoxelAnnotation


class MatplotlibPlotting(PlottingFrame, QWidget):

    def __init__(self, controller, parent=None, plotting_info_viewer=None):
        super().__init__(controller, plotting_info_viewer=plotting_info_viewer)

        self._controller.model_updated.connect(self.update_model)

        self._auto_render = True

        current_model = self._controller.get_model()

        self.figure = Figure(facecolor='#bfbfbf')
        self.visualizer = MapsVisualizer(current_model.get_data(), self.figure)
        self._axes_data = self.visualizer.render(current_model.get_config())

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()
        self.canvas.updateGeometry()

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.setParent(parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()

        self._redraw_timer = QTimer()
        self._redraw_timer.timeout.connect(self._timer_event)
        self._redraw_timer.timeout.connect(self._redraw_timer.stop)

        self._mouse_interaction = _MouseInteraction(self.figure, self._plotting_info_viewer, self._controller)
        self._mouse_interaction.update_axes_data(self._axes_data)

        self._previous_model = None
        self.setMinimumWidth(100)

    def export_image(self, filename, width, height, dpi=100):
        current_model = self._controller.get_model()

        width_inch = width / dpi
        height_inch = height / dpi

        figure = Figure(figsize=(width_inch, height_inch), dpi=dpi)
        visualizer = MapsVisualizer(current_model.get_data(), figure)
        FigureCanvas(figure)

        visualizer.to_file(filename, current_model.get_config(), dpi=dpi)

    def set_auto_rendering(self, auto_render):
        self._auto_render = auto_render

    def redraw(self):
        self._redraw()

    @pyqtSlot()
    def _timer_event(self):
        self._redraw()

    @pyqtSlot(DataConfigModel)
    def update_model(self, model):
        def update():
            self._previous_model = model
            self.visualizer = MapsVisualizer(model.get_data(), self.figure)
            if self._auto_render:
                self._redraw_timer.start(300)

        if not self._previous_model:
            update()
        elif model.get_config().visible_changes(self._previous_model.get_config()):
            update()
        elif model.get_data() != self._previous_model.get_data():
            update()

    def _redraw(self):
        current_model = self._controller.get_model()

        self.figure.clf()

        self._axes_data = self.visualizer.render(current_model.get_config())
        self._mouse_interaction.update_axes_data(self._axes_data)

        try:
            self.figure.canvas.draw()
        except ValueError as exception:
            logger = logging.getLogger(__name__)
            logger.error(exception)


class _MouseInteraction:

    def __init__(self, figure, plotting_info_viewer, controller):
        self.figure = figure
        self.plotting_info_viewer = plotting_info_viewer
        self.controller = controller

        self._axes_data = []
        self.figure.canvas.mpl_connect('button_press_event', self._button_pressed)
        self.figure.canvas.mpl_connect('button_release_event', self._button_released)
        self.figure.canvas.mpl_connect('motion_notify_event', self._mouse_motion)
        self.figure.canvas.mpl_connect('scroll_event', self._scroll_event)
        self.figure.canvas.mpl_connect('key_press_event', self._on_key_press)
        self.figure.canvas.mpl_connect('key_release_event', self._on_key_release)

        self._in_drag = False
        self._control_is_held = False

        self._scrolling_manager = _ScrollingManager(controller)
        self._dragging_manager = _DraggingManager(controller)

    def update_axes_data(self, axes_data):
        """Set the updated axes data. Needs to be called if the axes are updated.

        Args:
            axes_data (list of AxisData): the information about the axes
        """
        self._axes_data = axes_data

    def _button_pressed(self, event):
        self._dragging_manager.set_starting_point(event.xdata, event.ydata)

    def _button_released(self, event):
        if self._in_drag:
            self._in_drag = False
            return

        current_annotations = copy.copy(self.controller.get_model().get_config().annotations)

        def voxel_index_in_locations(voxel_index):
            for annotation in current_annotations:
                if annotation.voxel_index == voxel_index:
                    return True
            return False

        def get_existing_matching_annotation_index(voxel_index):
            for ind, annotation in enumerate(current_annotations):
                if annotation.voxel_index == voxel_index:
                    return ind
            raise ValueError('Matching annotation not found')

        if event.button == 1:
            axis_data = self._get_matching_axis_data(event.inaxes)
            if axis_data:
                x, y = int(np.round(event.xdata)), int(np.round(event.ydata))
                index = axis_data.coordinates_to_index(x, y)[:3]

                if voxel_index_in_locations(index):
                    del current_annotations[get_existing_matching_annotation_index(index)]
                elif self._control_is_held:
                    current_annotations.append(VoxelAnnotation(index))
                else:
                    if len(current_annotations):
                        current_annotations.pop()
                    current_annotations.append(VoxelAnnotation(index))

                self.controller.apply_action(SetAnnotations(current_annotations))
            else:
                if self._control_is_held:
                    self.controller.apply_action(SetAnnotations([]))
                else:
                    if len(current_annotations):
                        current_annotations.pop()
                    self.controller.apply_action(SetAnnotations(current_annotations))

    def _scroll_event(self, event):
        if event.inaxes:
            if event.button == 'up':
                self._scrolling_manager.add_up_scroll()
            else:
                self._scrolling_manager.add_down_scroll()

    def _mouse_motion(self, event):
        if event.button == 1:
            self._in_drag = True
            self._drag_images(event)
        else:
            self._update_info_box(event)

    def _on_key_press(self, event):
        if event.key == 'control':
            self._control_is_held = True

    def _on_key_release(self, event):
        if event.key == 'control':
            self._control_is_held = False

    def _drag_images(self, event):
        self._dragging_manager.mouse_moved(event.xdata, event.ydata)

    def _update_info_box(self, event):
        """Update the info box in the plotting info object.

        Args:
            event (MouseEvent): a matplotlib mouse event used to update the plotting info
        """
        axis_data = self._get_matching_axis_data(event.inaxes)
        if axis_data:
            x, y = int(np.round(event.xdata)), int(np.round(event.ydata))
            index = axis_data.coordinates_to_index(x, y)
            self.plotting_info_viewer.set_voxel_info(axis_data.map_name, (x, y), tuple(index))
        else:
            self.plotting_info_viewer.clear_voxel_info()

    def _get_matching_axis_data(self, axis):
        """Get the axis data matching the given axis.

        Args:
            axis: the matplotlib axis to match

        Returns:
            AxisData: our data container for that axis
        """
        if axis:
            for axes_data in self._axes_data:
                if axes_data.axis == axis:
                    return axes_data
        return None


class _DraggingManager:

    def __init__(self, controller):
        self.controller = controller

        self._start_x = 0
        self._start_y = 0
        self._end_x = 0
        self._end_y = 0

        self._drag_timer = QTimer()
        self._drag_timer.timeout.connect(self._perform_drag)
        self._drag_timer.timeout.connect(self._drag_timer.stop)

    def set_starting_point(self, x, y):
        self._start_x = x
        self._start_y = y

    def mouse_moved(self, x, y):
        if x is not None and y is not None:
            self._end_x = x
            self._end_y = y
            self._drag_timer.start(50)

    def _perform_drag(self):
        current_model = self.controller.get_model()

        delta_x = int(np.round(self._start_x) - np.round(self._end_x))
        delta_y = int(np.round(self._start_y) - np.round(self._end_y))

        config = current_model.get_config()
        data_info = current_model.get_data()

        current_zoom = current_model.get_config().zoom

        max_y = data_info.get_max_y_index(config.dimension, rotate=config.rotate, map_names=config.maps_to_show)
        max_x = data_info.get_max_x_index(config.dimension, rotate=config.rotate, map_names=config.maps_to_show)

        new_x0 = current_zoom.p0.x + delta_x
        new_x1 = (current_zoom.p1.x or max_x) + delta_x
        new_y0 = current_zoom.p0.y + delta_y
        new_y1 = (current_zoom.p1.y or max_y) + delta_y

        if new_x0 < 0:
            new_x1 -= new_x0
            new_x0 = 0

        if new_x1 > max_x:
            new_x0 -= new_x1
            new_x1 = max_x

        if new_y0 < 0:
            new_y1 -= new_y0
            new_y0 = 0

        if new_y1 > max_y:
            new_y0 -= new_y1
            new_y1 = max_y

        try:
            new_zoom = Zoom.from_coords(new_x0, new_y0, new_x1, new_y1)
        except ValueError:
            new_zoom = current_zoom

        self.controller.apply_action(SetZoom(new_zoom))
        self._start_x = self._end_x
        self._start_y = self._end_y


class _ScrollingManager:

    def __init__(self, controller):
        self.controller = controller

        self._scrolls = 0

        self._scroll_timer = QTimer()
        self._scroll_timer.timeout.connect(self._perform_scroll)
        self._scroll_timer.timeout.connect(self._scroll_timer.stop)

    def add_up_scroll(self):
        self._scrolls += 1
        self._scroll_timer.start(200)

    def add_down_scroll(self):
        self._scrolls -= 1
        self._scroll_timer.start(200)

    def _perform_scroll(self):
        current_model = self.controller.get_model()
        config = current_model.get_config()
        data_info = current_model.get_data()

        current_zoom = config.zoom

        max_y = data_info.get_max_y_index(config.dimension, rotate=config.rotate, map_names=config.maps_to_show)
        max_x = data_info.get_max_x_index(config.dimension, rotate=config.rotate, map_names=config.maps_to_show)

        scrolling = self._scrolls
        if abs(self._scrolls) > 1:
            scrolling *= 3

        new_x0 = current_zoom.p0.x + scrolling
        if new_x0 < 0:
            new_x0 = 0

        new_y0 = current_zoom.p0.y + scrolling
        if new_y0 < 0:
            new_y0 = 0

        new_x1 = (current_zoom.p1.x or max_x) - scrolling
        if new_x1 > max_x:
            new_x1 = max_x

        new_y1 = (current_zoom.p1.y or max_y) - scrolling
        if new_y1 > max_y:
            new_y1 = max_y

        try:
            new_zoom = Zoom.from_coords(new_x0, new_y0, new_x1, new_y1)
        except ValueError:
            new_zoom = current_zoom

        self.controller.apply_action(SetZoom(new_zoom))
        self._scrolls = 0
