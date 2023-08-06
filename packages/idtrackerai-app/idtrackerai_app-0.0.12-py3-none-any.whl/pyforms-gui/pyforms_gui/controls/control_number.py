#!/usr/bin/python
# -*- coding: utf-8 -*-


from confapp import conf

import pyforms_gui.utils.tools as tools

from AnyQt import uic

from pyforms_gui.controls.control_base import ControlBase


class ControlNumber(ControlBase):
    def __init__(self, *args, **kwargs):
        """
        :param int minimum: Minimum value.
        :param int maximum: Maximum value.
        :param float default: Set the value. Default = 0.
        :param int decimals: Decimals precision.
        :param float step: Step jump value.
        """
        self._min  = kwargs.get('minimum', 0)
        self._max  = kwargs.get('maximum', 100)
        if 'default' not in kwargs: kwargs['default'] = 0
        ControlBase.__init__(self, *args, **kwargs)
        self.decimals = kwargs.get('decimals', 0)
        self.step     = kwargs.get('step', 1)
        
    def init_form(self):
        control_path = tools.getFileInSameDirectory(__file__, "number.ui")
        self._form = uic.loadUi(control_path)
        self.min = self._min
        self.max = self._max
        self.label = self._label
        self.form.label.setAccessibleName('ControlNumber-label')
        self.form.spinBox.valueChanged.connect(self.update_event)

        self._update_slider = True
        self.form.spinBox.setValue(self._value)
        del self._update_slider

        super(ControlNumber, self).init_form()

        
    def update_event(self, value):
        if not hasattr(self, '_update_slider'):
            self.value = value

    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def label(self): return self.form.label.text()

    @label.setter
    def label(self, value): self.form.label.setText(value)

    @property
    def value(self):
        return self._value
        return self.form.spinBox.value()

    @value.setter
    def value(self, value):
        if value != self.value:
            self._update_slider = True
            self.form.spinBox.setValue(value)
            del self._update_slider

        ControlBase.value.fset(self, self.form.spinBox.value())

    @property
    def min(self): return self.form.spinBox.minimum()

    @min.setter
    def min(self, value): self.form.spinBox.setMinimum(value)

    @property
    def max(self): return self.form.spinBox.maximum()

    @max.setter
    def max(self, value): self.form.spinBox.setMaximum(value)

    @property
    def decimals(self): return self.form.spinBox.decimals()

    @decimals.setter
    def decimals(self, value): self.form.spinBox.setDecimals(value)

    @property
    def step(self): return self.form.spinBox.singleStep()

    @step.setter
    def step(self, value): self.form.spinBox.setSingleStep(value)   
