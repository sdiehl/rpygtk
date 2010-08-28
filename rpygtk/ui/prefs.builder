<?xml version="1.0"?>
<interface>
  <requires lib="gtk+" version="2.16"/>
  <!-- interface-naming-policy project-wide -->
  <object class="GtkDialog" id="preferences">
    <property name="border_width">5</property>
    <property name="window_position">center-on-parent</property>
    <property name="type_hint">normal</property>
    <property name="has_separator">False</property>
    <child internal-child="vbox">
      <object class="GtkVBox" id="dialog-vbox4">
        <property name="visible">True</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkNotebook" id="notebook_prefs">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <child>
              <object class="GtkTable" id="prefs_table1">
                <property name="visible">True</property>
                <property name="n_rows">4</property>
                <property name="n_columns">2</property>
                <child>
                  <object class="GtkCheckButton" id="auto_switch">
                    <property name="label" translatable="yes">Switch to data view when new object is created.</property>
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <property name="receives_default">False</property>
                    <property name="xalign">0.54000002145767212</property>
                    <property name="draw_indicator">True</property>
                  </object>
                  <packing>
                    <property name="right_attach">2</property>
                    <property name="top_attach">1</property>
                    <property name="bottom_attach">2</property>
                    <property name="x_options">GTK_FILL</property>
                    <property name="y_options">GTK_FILL</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkLabel" id="label1">
                    <property name="visible">True</property>
                    <property name="label" translatable="yes">Window Handling</property>
                    <attributes>
                      <attribute name="weight" value="bold"/>
                      <attribute name="underline" value="True"/>
                      <attribute name="gravity" value="east"/>
                    </attributes>
                  </object>
                  <packing>
                    <property name="x_options"></property>
                    <property name="y_options"></property>
                  </packing>
                </child>
                <child>
                  <object class="GtkLabel" id="label2">
                    <property name="visible">True</property>
                    <property name="label" translatable="yes">Appearance</property>
                    <attributes>
                      <attribute name="weight" value="bold"/>
                      <attribute name="underline" value="True"/>
                    </attributes>
                  </object>
                  <packing>
                    <property name="top_attach">2</property>
                    <property name="bottom_attach">3</property>
                    <property name="x_options"></property>
                    <property name="y_options"></property>
                  </packing>
                </child>
                <child>
                  <object class="GtkFontButton" id="font">
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <property name="receives_default">True</property>
                    <property name="font_name">Monospace 12</property>
                  </object>
                  <packing>
                    <property name="left_attach">1</property>
                    <property name="right_attach">2</property>
                    <property name="top_attach">3</property>
                    <property name="bottom_attach">4</property>
                    <property name="x_options">GTK_FILL</property>
                    <property name="y_options"></property>
                    <property name="x_padding">25</property>
                    <property name="y_padding">25</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkLabel" id="label3">
                    <property name="visible">True</property>
                    <property name="label" translatable="yes">Data Font</property>
                  </object>
                  <packing>
                    <property name="top_attach">3</property>
                    <property name="bottom_attach">4</property>
                  </packing>
                </child>
                <child>
                  <placeholder/>
                </child>
                <child>
                  <placeholder/>
                </child>
              </object>
            </child>
            <child type="tab">
              <object class="GtkLabel" id="general_prefs">
                <property name="visible">True</property>
                <property name="label" translatable="yes">General</property>
              </object>
              <packing>
                <property name="tab_fill">False</property>
              </packing>
            </child>
            <child>
              <object class="GtkTable" id="prefs_table3">
                <property name="visible">True</property>
                <property name="n_rows">3</property>
                <property name="n_columns">2</property>
                <child>
                  <object class="GtkCheckButton" id="single_plot">
                    <property name="label" translatable="yes">Use single plot window.</property>
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <property name="receives_default">False</property>
                    <property name="draw_indicator">True</property>
                  </object>
                  <packing>
                    <property name="right_attach">2</property>
                    <property name="x_options">GTK_FILL</property>
                    <property name="y_options">GTK_FILL</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkCheckButton" id="close_plots">
                    <property name="label" translatable="yes">Close plot windows after plot dialog is closed.</property>
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <property name="receives_default">False</property>
                    <property name="draw_indicator">True</property>
                  </object>
                  <packing>
                    <property name="right_attach">2</property>
                    <property name="top_attach">1</property>
                    <property name="bottom_attach">2</property>
                    <property name="x_options">GTK_FILL</property>
                    <property name="y_options">GTK_FILL</property>
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
                <property name="position">1</property>
              </packing>
            </child>
            <child type="tab">
              <object class="GtkLabel" id="plotting_prefs">
                <property name="visible">True</property>
                <property name="label" translatable="yes">Plotting</property>
              </object>
              <packing>
                <property name="position">1</property>
                <property name="tab_fill">False</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child internal-child="action_area">
          <object class="GtkHButtonBox" id="dialog-action_area4">
            <property name="visible">True</property>
            <property name="layout_style">end</property>
            <child>
              <object class="GtkButton" id="cancel">
                <property name="label">gtk-cancel</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_stock">True</property>
                <signal name="clicked" handler="hide"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="apply_prefs">
                <property name="label">gtk-apply</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_stock">True</property>
                <signal name="clicked" handler="apply"/>
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
            <property name="pack_type">end</property>
            <property name="position">0</property>
          </packing>
        </child>
      </object>
    </child>
    <action-widgets>
      <action-widget response="0">cancel</action-widget>
      <action-widget response="0">apply_prefs</action-widget>
    </action-widgets>
  </object>
</interface>
