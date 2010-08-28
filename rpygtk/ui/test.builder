<?xml version="1.0"?>
<interface>
  <requires lib="gtk+" version="2.16"/>
  <!-- interface-naming-policy project-wide -->
  <object class="GtkVBox" id="test_vbox">
    <property name="visible">True</property>
    <property name="orientation">vertical</property>
    <property name="spacing">10</property>
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
                        <signal name="add" handler="shrink_window"/>
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
                    <property name="padding">10</property>
                    <property name="position">0</property>
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
            <property name="label" translatable="yes">Variables/Data</property>
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
                <property name="spacing">10</property>
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
          <object class="GtkLabel" id="label1">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Parameters</property>
          </object>
          <packing>
            <property name="position">1</property>
            <property name="tab_fill">False</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="expand">False</property>
        <property name="padding">10</property>
        <property name="position">0</property>
      </packing>
    </child>
    <child>
      <object class="GtkButton" id="runbutton">
        <property name="label" translatable="yes">Run</property>
        <property name="height_request">52</property>
        <property name="visible">True</property>
        <property name="can_focus">True</property>
        <property name="receives_default">True</property>
        <property name="use_underline">True</property>
        <property name="image_position">top</property>
      </object>
      <packing>
        <property name="expand">False</property>
        <property name="fill">False</property>
        <property name="position">1</property>
      </packing>
    </child>
  </object>
</interface>
