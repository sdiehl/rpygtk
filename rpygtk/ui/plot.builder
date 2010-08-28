<?xml version="1.0"?>
<interface>
  <requires lib="gtk+" version="2.16"/>
  <!-- interface-naming-policy toplevel-contextual -->
  <object class="GtkListStore" id="fill_types">
    <columns>
      <!-- column-name gchararray1 -->
      <column type="gchararray"/>
    </columns>
    <data>
      <row>
        <col id="0" translatable="yes">Solid</col>
      </row>
      <row>
        <col id="0" translatable="yes">Rainbow</col>
      </row>
      <row>
        <col id="0" translatable="yes">Gray</col>
      </row>
    </data>
  </object>
  <object class="GtkListStore" id="liststore1">
    <columns>
      <!-- column-name gchararray1 -->
      <column type="gchararray"/>
    </columns>
    <data>
      <row>
        <col id="0" translatable="yes">&#x25AB;</col>
      </row>
      <row>
        <col id="0" translatable="yes">&#x25CB;</col>
      </row>
      <row>
        <col id="0" translatable="yes">&#x25B3;</col>
      </row>
      <row>
        <col id="0" translatable="yes">+</col>
      </row>
      <row>
        <col id="0" translatable="yes">&#x2A2F;</col>
      </row>
      <row>
        <col id="0" translatable="yes">&#x2B20;</col>
      </row>
      <row>
        <col id="0" translatable="yes">&#x25BD;</col>
      </row>
      <row>
        <col id="0" translatable="yes">&#x25B4;</col>
      </row>
    </data>
  </object>
  <object class="GtkListStore" id="line_types">
    <columns>
      <!-- column-name images -->
      <column type="GdkPixbuf"/>
    </columns>
    <data>
      <row>
        <col id="0">icons/line_solid.svg</col>
      </row>
      <row>
        <col id="0">icons/line_dash.svg</col>
      </row>
      <row>
        <col id="0">icons/line_dot.svg</col>
      </row>
      <row>
        <col id="0">icons/line_dotdash.svg</col>
      </row>
      <row>
        <col id="0">icons/line_longdash.svg</col>
      </row>
    </data>
  </object>
  <object class="GtkListStore" id="frame_styles">
    <columns>
      <!-- column-name images -->
      <column type="GdkPixbuf"/>
    </columns>
    <data>
      <row>
        <col id="0">icons/frame_n.svg</col>
      </row>
      <row>
        <col id="0">icons/frame_o.svg</col>
      </row>
      <row>
        <col id="0">icons/frame_l.svg</col>
      </row>
      <row>
        <col id="0">icons/frame_7.svg</col>
      </row>
      <row>
        <col id="0">icons/frame_c.svg</col>
      </row>
      <row>
        <col id="0">icons/frame_u.svg</col>
      </row>
      <row>
        <col id="0">icons/frame_].svg</col>
      </row>
    </data>
  </object>
  <object class="GtkVBox" id="plotview">
    <property name="visible">True</property>
    <property name="orientation">vertical</property>
    <property name="spacing">10</property>
    <child>
      <object class="GtkNotebook" id="pars">
        <property name="visible">True</property>
        <property name="can_focus">True</property>
        <signal name="switch_page" handler="shrink_window"/>
        <signal name="select_page" handler="shrink_window"/>
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
                  <object class="GtkFrame" id="data_single">
                    <property name="visible">True</property>
                    <property name="label_xalign">0</property>
                    <property name="shadow_type">none</property>
                    <child>
                      <object class="GtkHBox" id="hbox">
                        <property name="visible">True</property>
                        <property name="spacing">10</property>
                        <child>
                          <object class="GtkVBox" id="vbox11">
                            <property name="visible">True</property>
                            <property name="border_width">1</property>
                            <property name="orientation">vertical</property>
                            <child>
                              <object class="GtkLabel" id="label3">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">x-Axis</property>
                                <attributes>
                                  <attribute name="underline" value="True"/>
                                </attributes>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="position">0</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkScrolledWindow" id="scrolledwindow21">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="hscrollbar_policy">automatic</property>
                                <property name="vscrollbar_policy">automatic</property>
                                <child>
                                  <object class="GtkTreeView" id="variable1">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="headers_visible">False</property>
                                  </object>
                                </child>
                              </object>
                              <packing>
                                <property name="position">1</property>
                              </packing>
                            </child>
                          </object>
                          <packing>
                            <property name="position">0</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkVBox" id="vbox12">
                            <property name="visible">True</property>
                            <property name="border_width">1</property>
                            <property name="orientation">vertical</property>
                            <child>
                              <object class="GtkLabel" id="label16">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">y-Axis</property>
                                <attributes>
                                  <attribute name="underline" value="True"/>
                                </attributes>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="position">0</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkScrolledWindow" id="scrolledwindow31">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="hscrollbar_policy">automatic</property>
                                <property name="vscrollbar_policy">automatic</property>
                                <child>
                                  <object class="GtkTreeView" id="variable2">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="headers_visible">False</property>
                                  </object>
                                </child>
                              </object>
                              <packing>
                                <property name="position">1</property>
                              </packing>
                            </child>
                          </object>
                          <packing>
                            <property name="position">1</property>
                          </packing>
                        </child>
                      </object>
                    </child>
                    <child type="label">
                      <object class="GtkLabel" id="label1">
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
                <child>
                  <object class="GtkFrame" id="data_multiple">
                    <property name="visible">True</property>
                    <property name="label_xalign">0</property>
                    <property name="shadow_type">none</property>
                    <child>
                      <object class="GtkTable" id="table1">
                        <property name="visible">True</property>
                        <property name="n_rows">3</property>
                        <property name="n_columns">2</property>
                        <property name="column_spacing">2</property>
                        <child>
                          <object class="GtkButton" id="add_variable">
                            <property name="label">gtk-add</property>
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="receives_default">True</property>
                            <property name="use_stock">True</property>
                            <property name="image_position">right</property>
                          </object>
                          <packing>
                            <property name="top_attach">2</property>
                            <property name="bottom_attach">3</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkLabel" id="label18">
                            <property name="visible">True</property>
                            <property name="label" translatable="yes">Variable</property>
                            <attributes>
                              <attribute name="underline" value="True"/>
                            </attributes>
                          </object>
                        </child>
                        <child>
                          <object class="GtkLabel" id="label19">
                            <property name="visible">True</property>
                            <property name="label" translatable="yes">Active Variables</property>
                            <attributes>
                              <attribute name="underline" value="True"/>
                            </attributes>
                          </object>
                          <packing>
                            <property name="left_attach">1</property>
                            <property name="right_attach">2</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkScrolledWindow" id="scrolledwindow2">
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="hscrollbar_policy">automatic</property>
                            <property name="vscrollbar_policy">automatic</property>
                            <child>
                              <object class="GtkTreeView" id="variables">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="headers_visible">False</property>
                                <property name="rubber_banding">True</property>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="top_attach">1</property>
                            <property name="bottom_attach">2</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkScrolledWindow" id="scrolledwindow3">
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="hscrollbar_policy">automatic</property>
                            <property name="vscrollbar_policy">automatic</property>
                            <child>
                              <object class="GtkTreeView" id="active_variables">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="headers_visible">False</property>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="left_attach">1</property>
                            <property name="right_attach">2</property>
                            <property name="top_attach">1</property>
                            <property name="bottom_attach">2</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkButton" id="del_variable">
                            <property name="label">gtk-remove</property>
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="receives_default">True</property>
                            <property name="use_stock">True</property>
                            <property name="image_position">right</property>
                          </object>
                          <packing>
                            <property name="left_attach">1</property>
                            <property name="right_attach">2</property>
                            <property name="top_attach">2</property>
                            <property name="bottom_attach">3</property>
                          </packing>
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
                    <property name="position">1</property>
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
          <object class="GtkViewport" id="viewport5">
            <property name="visible">True</property>
            <property name="resize_mode">queue</property>
            <child>
              <object class="GtkVBox" id="vbox2">
                <property name="visible">True</property>
                <property name="orientation">vertical</property>
                <child>
                  <object class="GtkHBox" id="hbox2">
                    <property name="visible">True</property>
                    <property name="spacing">10</property>
                    <child>
                      <object class="GtkFrame" id="frame1">
                        <property name="visible">True</property>
                        <property name="label_xalign">0</property>
                        <property name="shadow_type">none</property>
                        <child>
                          <object class="GtkTable" id="table2">
                            <property name="visible">True</property>
                            <property name="n_rows">3</property>
                            <property name="n_columns">3</property>
                            <child>
                              <object class="GtkLabel" id="label5">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">X Range:</property>
                              </object>
                              <packing>
                                <property name="x_options">GTK_FILL</property>
                                <property name="y_options">GTK_FILL</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkLabel" id="label6">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Y Range:</property>
                              </object>
                              <packing>
                                <property name="top_attach">1</property>
                                <property name="bottom_attach">2</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkEntry" id="xmin">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="invisible_char">&#x25CF;</property>
                                <property name="width_chars">4</property>
                              </object>
                              <packing>
                                <property name="left_attach">1</property>
                                <property name="right_attach">2</property>
                                <property name="x_options">GTK_EXPAND | GTK_SHRINK | GTK_FILL</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkEntry" id="xmax">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="invisible_char">&#x25CF;</property>
                                <property name="width_chars">4</property>
                              </object>
                              <packing>
                                <property name="left_attach">2</property>
                                <property name="right_attach">3</property>
                                <property name="x_options">GTK_EXPAND | GTK_SHRINK | GTK_FILL</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkEntry" id="ymin">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="invisible_char">&#x25CF;</property>
                                <property name="width_chars">4</property>
                              </object>
                              <packing>
                                <property name="left_attach">1</property>
                                <property name="right_attach">2</property>
                                <property name="top_attach">1</property>
                                <property name="bottom_attach">2</property>
                                <property name="x_options">GTK_EXPAND | GTK_SHRINK | GTK_FILL</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkEntry" id="ymax">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="invisible_char">&#x25CF;</property>
                                <property name="width_chars">4</property>
                              </object>
                              <packing>
                                <property name="left_attach">2</property>
                                <property name="right_attach">3</property>
                                <property name="top_attach">1</property>
                                <property name="bottom_attach">2</property>
                                <property name="x_options">GTK_EXPAND | GTK_SHRINK | GTK_FILL</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkCheckButton" id="automanage">
                                <property name="label" translatable="yes">Auto Detect Range</property>
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="receives_default">False</property>
                                <property name="active">True</property>
                                <property name="draw_indicator">True</property>
                              </object>
                              <packing>
                                <property name="right_attach">3</property>
                                <property name="top_attach">2</property>
                                <property name="bottom_attach">3</property>
                              </packing>
                            </child>
                          </object>
                        </child>
                        <child type="label">
                          <object class="GtkLabel" id="label4">
                            <property name="visible">True</property>
                            <property name="label" translatable="yes">&lt;b&gt;Range&lt;/b&gt;</property>
                            <property name="use_markup">True</property>
                          </object>
                        </child>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">False</property>
                        <property name="padding">10</property>
                        <property name="position">0</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkFrame" id="frame2">
                        <property name="visible">True</property>
                        <property name="label_xalign">0</property>
                        <property name="shadow_type">none</property>
                        <child>
                          <object class="GtkAlignment" id="alignment1">
                            <property name="visible">True</property>
                            <child>
                              <object class="GtkTable" id="table3">
                                <property name="visible">True</property>
                                <property name="n_rows">3</property>
                                <property name="n_columns">3</property>
                                <child>
                                  <object class="GtkLabel" id="label8">
                                    <property name="visible">True</property>
                                    <property name="label" translatable="yes">X</property>
                                  </object>
                                </child>
                                <child>
                                  <object class="GtkLabel" id="label9">
                                    <property name="visible">True</property>
                                    <property name="label" translatable="yes">Y</property>
                                  </object>
                                  <packing>
                                    <property name="top_attach">1</property>
                                    <property name="bottom_attach">2</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkLabel" id="label10">
                                    <property name="visible">True</property>
                                    <property name="label" translatable="yes">Title</property>
                                  </object>
                                  <packing>
                                    <property name="top_attach">2</property>
                                    <property name="bottom_attach">3</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkEntry" id="xlab">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="invisible_char">&#x25CF;</property>
                                  </object>
                                  <packing>
                                    <property name="left_attach">1</property>
                                    <property name="right_attach">2</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkEntry" id="ylab">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="invisible_char">&#x25CF;</property>
                                  </object>
                                  <packing>
                                    <property name="left_attach">1</property>
                                    <property name="right_attach">2</property>
                                    <property name="top_attach">1</property>
                                    <property name="bottom_attach">2</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkEntry" id="title">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="invisible_char">&#x25CF;</property>
                                  </object>
                                  <packing>
                                    <property name="left_attach">1</property>
                                    <property name="right_attach">2</property>
                                    <property name="top_attach">2</property>
                                    <property name="bottom_attach">3</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="exp1">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="draw_indicator">True</property>
                                  </object>
                                  <packing>
                                    <property name="left_attach">2</property>
                                    <property name="right_attach">3</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="exp2">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="draw_indicator">True</property>
                                  </object>
                                  <packing>
                                    <property name="left_attach">2</property>
                                    <property name="right_attach">3</property>
                                    <property name="top_attach">1</property>
                                    <property name="bottom_attach">2</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="exp3">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="draw_indicator">True</property>
                                  </object>
                                  <packing>
                                    <property name="left_attach">2</property>
                                    <property name="right_attach">3</property>
                                    <property name="top_attach">2</property>
                                    <property name="bottom_attach">3</property>
                                  </packing>
                                </child>
                              </object>
                            </child>
                          </object>
                        </child>
                        <child type="label">
                          <object class="GtkLabel" id="label7">
                            <property name="visible">True</property>
                            <property name="label" translatable="yes">&lt;b&gt;Axis Labels&lt;/b&gt;</property>
                            <property name="use_markup">True</property>
                          </object>
                        </child>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">False</property>
                        <property name="padding">10</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                    <child>
                      <placeholder/>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">False</property>
                    <property name="padding">10</property>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkFrame" id="frame3">
                    <property name="label_xalign">0</property>
                    <property name="shadow_type">none</property>
                    <child>
                      <object class="GtkAlignment" id="alignment5">
                        <property name="visible">True</property>
                        <property name="left_padding">12</property>
                        <child>
                          <placeholder/>
                        </child>
                      </object>
                    </child>
                    <child type="label">
                      <object class="GtkLabel" id="label15">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">&lt;b&gt;Orientation&lt;/b&gt;</property>
                        <property name="use_markup">True</property>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="position">1</property>
                  </packing>
                </child>
                <child>
                  <placeholder/>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="position">1</property>
            <property name="tab_fill">False</property>
          </packing>
        </child>
        <child type="tab">
          <object class="GtkLabel" id="label12">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Labels</property>
          </object>
          <packing>
            <property name="position">5</property>
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
                    <property name="spacing">10</property>
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
                    <property name="padding">10</property>
                    <property name="position">0</property>
                  </packing>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="position">2</property>
          </packing>
        </child>
        <child type="tab">
          <object class="GtkLabel" id="label20">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Parameters</property>
          </object>
          <packing>
            <property name="position">2</property>
            <property name="tab_fill">False</property>
          </packing>
        </child>
        <child>
          <object class="GtkViewport" id="viewport2">
            <property name="visible">True</property>
            <property name="resize_mode">queue</property>
            <child>
              <object class="GtkVBox" id="vbox5">
                <property name="visible">True</property>
                <property name="orientation">vertical</property>
                <child>
                  <object class="GtkHBox" id="advparams">
                    <property name="visible">True</property>
                    <property name="spacing">10</property>
                    <child>
                      <object class="GtkVBox" id="vbox3_obj">
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
                      <object class="GtkVBox" id="vbox4_obj">
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
                    <property name="padding">10</property>
                    <property name="position">0</property>
                  </packing>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="position">3</property>
          </packing>
        </child>
        <child type="tab">
          <object class="GtkLabel" id="advparms_tab">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Advanced Parameters</property>
          </object>
          <packing>
            <property name="position">3</property>
            <property name="tab_fill">False</property>
          </packing>
        </child>
        <child>
          <object class="GtkViewport" id="viewport3">
            <property name="visible">True</property>
            <property name="resize_mode">queue</property>
            <child>
              <object class="GtkVBox" id="vbox3">
                <property name="visible">True</property>
                <property name="orientation">vertical</property>
                <child>
                  <object class="GtkHBox" id="hbox3">
                    <property name="visible">True</property>
                    <property name="spacing">10</property>
                    <child>
                      <object class="GtkFrame" id="points_frame">
                        <property name="visible">True</property>
                        <property name="label_xalign">0</property>
                        <property name="shadow_type">none</property>
                        <child>
                          <object class="GtkAlignment" id="alignment2">
                            <property name="visible">True</property>
                            <property name="left_padding">12</property>
                            <child>
                              <object class="GtkVBox" id="vbox13543">
                                <property name="visible">True</property>
                                <property name="orientation">vertical</property>
                                <child>
                                  <object class="GtkComboBox" id="point_style">
                                    <property name="visible">True</property>
                                    <property name="model">liststore1</property>
                                    <property name="active">1</property>
                                    <child>
                                      <object class="GtkCellRendererText" id="types"/>
                                      <attributes>
                                        <attribute name="text">0</attribute>
                                      </attributes>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="position">0</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkColorButton" id="point_color">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">True</property>
                                    <property name="use_alpha">True</property>
                                    <property name="title" translatable="yes">Point Color</property>
                                    <property name="color">#000000000000</property>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="position">1</property>
                                  </packing>
                                </child>
                              </object>
                            </child>
                          </object>
                        </child>
                        <child type="label">
                          <object class="GtkLabel" id="label13">
                            <property name="visible">True</property>
                            <property name="label" translatable="yes">&lt;b&gt;Points&lt;/b&gt;</property>
                            <property name="use_markup">True</property>
                          </object>
                        </child>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">False</property>
                        <property name="position">0</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkFrame" id="lines_frame">
                        <property name="visible">True</property>
                        <property name="label_xalign">0</property>
                        <property name="shadow_type">none</property>
                        <child>
                          <object class="GtkAlignment" id="alignment3">
                            <property name="visible">True</property>
                            <property name="left_padding">12</property>
                            <child>
                              <object class="GtkVBox" id="line_controls">
                                <property name="visible">True</property>
                                <property name="orientation">vertical</property>
                                <child>
                                  <object class="GtkComboBox" id="line_style">
                                    <property name="visible">True</property>
                                    <property name="model">line_types</property>
                                    <property name="active">0</property>
                                    <child>
                                      <object class="GtkCellRendererPixbuf" id="cellrenderertext1"/>
                                      <attributes>
                                        <attribute name="pixbuf">0</attribute>
                                      </attributes>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="position">0</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkColorButton" id="line_color">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">True</property>
                                    <property name="use_alpha">True</property>
                                    <property name="title" translatable="yes">Line Color</property>
                                    <property name="color">#000000000000</property>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="fill">False</property>
                                    <property name="position">1</property>
                                  </packing>
                                </child>
                              </object>
                            </child>
                          </object>
                        </child>
                        <child type="label">
                          <object class="GtkLabel" id="label14">
                            <property name="visible">True</property>
                            <property name="label" translatable="yes">&lt;b&gt;Lines&lt;/b&gt;</property>
                            <property name="use_markup">True</property>
                          </object>
                        </child>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">False</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkFrame" id="fill_frame">
                        <property name="visible">True</property>
                        <property name="label_xalign">0</property>
                        <property name="shadow_type">none</property>
                        <child>
                          <object class="GtkAlignment" id="alignment4">
                            <property name="visible">True</property>
                            <property name="left_padding">12</property>
                            <child>
                              <object class="GtkVBox" id="fill_controlls">
                                <property name="visible">True</property>
                                <property name="orientation">vertical</property>
                                <child>
                                  <object class="GtkComboBox" id="fill_style">
                                    <property name="visible">True</property>
                                    <property name="model">fill_types</property>
                                    <property name="active">0</property>
                                    <signal name="changed" handler="fill_handler"/>
                                    <child>
                                      <object class="GtkCellRendererText" id="fill_column"/>
                                      <attributes>
                                        <attribute name="text">0</attribute>
                                      </attributes>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="position">0</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkColorButton" id="fill_color">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">True</property>
                                    <property name="use_alpha">True</property>
                                    <property name="title" translatable="yes">Fill Color</property>
                                    <property name="color">#ffffffffffff</property>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="fill">False</property>
                                    <property name="position">1</property>
                                  </packing>
                                </child>
                              </object>
                            </child>
                          </object>
                        </child>
                        <child type="label">
                          <object class="GtkLabel" id="label2">
                            <property name="visible">True</property>
                            <property name="label" translatable="yes">&lt;b&gt;Fill&lt;/b&gt;</property>
                            <property name="use_markup">True</property>
                          </object>
                        </child>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">False</property>
                        <property name="position">2</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkFrame" id="frame_frame">
                        <property name="visible">True</property>
                        <property name="label_xalign">0</property>
                        <property name="shadow_type">none</property>
                        <child>
                          <object class="GtkAlignment" id="alignment6">
                            <property name="visible">True</property>
                            <property name="left_padding">12</property>
                            <child>
                              <object class="GtkComboBox" id="frame_style">
                                <property name="visible">True</property>
                                <property name="model">frame_styles</property>
                                <property name="active">1</property>
                                <child>
                                  <object class="GtkCellRendererPixbuf" id="cellrenderertext2"/>
                                  <attributes>
                                    <attribute name="pixbuf">0</attribute>
                                  </attributes>
                                </child>
                              </object>
                            </child>
                          </object>
                        </child>
                        <child type="label">
                          <object class="GtkLabel" id="label23">
                            <property name="visible">True</property>
                            <property name="label" translatable="yes">&lt;b&gt;Frame&lt;/b&gt;</property>
                            <property name="use_markup">True</property>
                          </object>
                        </child>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">False</property>
                        <property name="position">3</property>
                      </packing>
                    </child>
                    <child>
                      <placeholder/>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="padding">10</property>
                    <property name="position">0</property>
                  </packing>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="position">4</property>
          </packing>
        </child>
        <child type="tab">
          <object class="GtkLabel" id="label21">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Appearance</property>
          </object>
          <packing>
            <property name="position">4</property>
            <property name="tab_fill">False</property>
          </packing>
        </child>
        <child>
          <object class="GtkViewport" id="viewport4">
            <property name="visible">True</property>
            <property name="resize_mode">queue</property>
            <child>
              <object class="GtkVBox" id="vbox1">
                <property name="visible">True</property>
                <property name="orientation">vertical</property>
                <child>
                  <object class="GtkButton" id="export_as_image">
                    <property name="label" translatable="yes">Export as Image</property>
                    <property name="height_request">35</property>
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <property name="receives_default">True</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">False</property>
                    <property name="padding">10</property>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkButton" id="export_to_workspace">
                    <property name="label" translatable="yes">Export to Workspace</property>
                    <property name="height_request">35</property>
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <property name="receives_default">True</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">False</property>
                    <property name="padding">10</property>
                    <property name="position">1</property>
                  </packing>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="position">5</property>
          </packing>
        </child>
        <child type="tab">
          <object class="GtkLabel" id="label22">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Export</property>
          </object>
          <packing>
            <property name="position">5</property>
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
      <object class="GtkButton" id="plotbutton">
        <property name="label" translatable="yes">Plot</property>
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
