<?xml version="1.0"?>
<interface>
  <requires lib="gtk+" version="2.16"/>
  <!-- interface-naming-policy project-wide -->
  <object class="GtkAdjustment" id="degree">
    <property name="value">1</property>
    <property name="lower">1</property>
    <property name="upper">10</property>
  </object>
  <object class="GtkVBox" id="regression_vbox">
    <property name="visible">True</property>
    <property name="orientation">vertical</property>
    <child>
      <object class="GtkNotebook" id="pars">
        <property name="visible">True</property>
        <property name="can_focus">True</property>
        <child>
          <object class="GtkViewport" id="viewport6">
            <property name="visible">True</property>
            <property name="resize_mode">queue</property>
            <child>
              <object class="GtkVBox" id="data_frames">
                <property name="visible">True</property>
                <property name="orientation">vertical</property>
                <property name="spacing">10</property>
                <child>
                  <object class="GtkFrame" id="data">
                    <property name="visible">True</property>
                    <property name="label_xalign">0</property>
                    <property name="shadow_type">none</property>
                    <child>
                      <object class="GtkHBox" id="custom_variables">
                        <property name="visible">True</property>
                        <property name="spacing">10</property>
                        <property name="homogeneous">True</property>
                        <child>
                          <object class="GtkScrolledWindow" id="scrolledwindow1">
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="hscrollbar_policy">automatic</property>
                            <property name="vscrollbar_policy">automatic</property>
                            <child>
                              <object class="GtkTreeView" id="variables">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="headers_visible">False</property>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="position">0</property>
                          </packing>
                        </child>
                        <child>
                          <placeholder/>
                        </child>
                      </object>
                    </child>
                    <child type="label">
                      <object class="GtkLabel" id="label17">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">&lt;b&gt;Data&lt;/b&gt;</property>
                        <property name="use_markup">True</property>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkFrame" id="degree_frame">
                    <property name="visible">True</property>
                    <property name="label_xalign">0</property>
                    <property name="shadow_type">none</property>
                    <child>
                      <object class="GtkAlignment" id="alignment2">
                        <property name="visible">True</property>
                        <property name="left_padding">12</property>
                        <child>
                          <object class="GtkHScale" id="degree_slider">
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="adjustment">degree</property>
                            <property name="fill_level">10</property>
                            <property name="digits">0</property>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child type="label">
                      <object class="GtkLabel" id="label3">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">&lt;b&gt;Degree&lt;/b&gt;</property>
                        <property name="use_markup">True</property>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="fill">False</property>
                    <property name="padding">10</property>
                    <property name="position">1</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkFrame" id="model_frame">
                    <property name="visible">True</property>
                    <property name="label_xalign">0</property>
                    <property name="shadow_type">none</property>
                    <child>
                      <object class="GtkHBox" id="hbox1">
                        <property name="visible">True</property>
                        <property name="orientation">vertical</property>
                        <child>
                          <object class="GtkScrolledWindow" id="scrolledwindow2">
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="hscrollbar_policy">automatic</property>
                            <property name="vscrollbar_policy">automatic</property>
                            <child>
                              <object class="GtkTreeView" id="preset_models">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="headers_visible">False</property>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="position">0</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkAlignment" id="custom_model">
                            <property name="visible">True</property>
                            <child>
                              <placeholder/>
                            </child>
                          </object>
                          <packing>
                            <property name="position">1</property>
                          </packing>
                        </child>
                      </object>
                    </child>
                    <child type="label">
                      <object class="GtkLabel" id="label9">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">&lt;b&gt;Model&lt;/b&gt;</property>
                        <property name="use_markup">True</property>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="position">2</property>
                  </packing>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="tab_fill">False</property>
          </packing>
        </child>
        <child type="tab">
          <object class="GtkLabel" id="label11">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Model</property>
          </object>
          <packing>
            <property name="tab_fill">False</property>
          </packing>
        </child>
        <child>
          <object class="GtkViewport" id="viewport1">
            <property name="visible">True</property>
            <property name="resize_mode">queue</property>
            <child>
              <object class="GtkVBox" id="vbox4">
                <property name="visible">True</property>
                <property name="orientation">vertical</property>
                <child>
                  <object class="GtkHBox" id="params_objects1">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkVBox" id="vbox1_obj">
                        <property name="visible">True</property>
                        <property name="orientation">vertical</property>
                        <child>
                          <placeholder/>
                        </child>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">False</property>
                        <property name="position">0</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkVBox" id="vbox2_obj">
                        <property name="visible">True</property>
                        <property name="orientation">vertical</property>
                        <child>
                          <placeholder/>
                        </child>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">False</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">False</property>
                    <property name="position">0</property>
                  </packing>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="position">1</property>
          </packing>
        </child>
        <child type="tab">
          <object class="GtkLabel" id="label2">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Parameters</property>
          </object>
          <packing>
            <property name="position">1</property>
            <property name="tab_fill">False</property>
          </packing>
        </child>
        <child>
          <object class="GtkViewport" id="viewport2">
            <property name="visible">True</property>
            <property name="resize_mode">queue</property>
            <child>
              <object class="GtkFrame" id="frame1">
                <property name="visible">True</property>
                <property name="label_xalign">0</property>
                <property name="shadow_type">none</property>
                <child>
                  <object class="GtkAlignment" id="alignment1">
                    <property name="visible">True</property>
                    <property name="left_padding">12</property>
                    <child>
                      <object class="GtkVBox" id="vbox1">
                        <property name="visible">True</property>
                        <property name="orientation">vertical</property>
                        <child>
                          <object class="GtkButton" id="exportmodelbutton">
                            <property name="label" translatable="yes">Export Model to Workspace</property>
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="receives_default">True</property>
                          </object>
                          <packing>
                            <property name="expand">False</property>
                            <property name="position">0</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkButton" id="exportfitbutton">
                            <property name="label" translatable="yes">Export Fit as Image</property>
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="receives_default">True</property>
                          </object>
                          <packing>
                            <property name="expand">False</property>
                            <property name="position">1</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkButton" id="exportsummarybutton">
                            <property name="label" translatable="yes">Export Summary of Fit as Image</property>
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="receives_default">True</property>
                          </object>
                          <packing>
                            <property name="expand">False</property>
                            <property name="position">2</property>
                          </packing>
                        </child>
                      </object>
                    </child>
                  </object>
                </child>
                <child type="label">
                  <object class="GtkLabel" id="label4">
                    <property name="visible">True</property>
                    <property name="label" translatable="yes">&lt;b&gt;Export to Workspace&lt;/b&gt;</property>
                    <property name="use_markup">True</property>
                  </object>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="position">2</property>
          </packing>
        </child>
        <child type="tab">
          <object class="GtkLabel" id="label1">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Export</property>
          </object>
          <packing>
            <property name="position">2</property>
            <property name="tab_fill">False</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="expand">False</property>
        <property name="padding">15</property>
        <property name="position">0</property>
      </packing>
    </child>
    <child>
      <object class="GtkTable" id="table1">
        <property name="visible">True</property>
        <property name="n_rows">2</property>
        <property name="n_columns">2</property>
        <child>
          <object class="GtkButton" id="plotfitbutton">
            <property name="label" translatable="yes">Plot Regression</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
          </object>
        </child>
        <child>
          <object class="GtkButton" id="plotsummarybutton">
            <property name="label" translatable="yes">Summary of Fit</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
          </object>
          <packing>
            <property name="left_attach">1</property>
            <property name="right_attach">2</property>
          </packing>
        </child>
        <child>
          <placeholder/>
        </child>
        <child>
          <placeholder/>
        </child>
      </object>
      <packing>
        <property name="expand">False</property>
        <property name="padding">10</property>
        <property name="position">1</property>
      </packing>
    </child>
  </object>
</interface>
