<?xml version="1.0"?>
<interface>
  <requires lib="gtk+" version="2.16"/>
  <!-- interface-naming-policy toplevel-contextual -->
  <!-- interface-local-resource-path /home/stephen/SVN/rpygtk/rpygtk/ui/icons/ -->
  <object class="GtkWindow" id="main">
    <property name="default_width">800</property>
    <property name="default_height">601</property>
    <property name="icon_name">applications-utilities</property>
    <signal name="destroy" handler="destroy"/>
    <signal name="window_state_event" handler="resize_object_pane"/>
    <child>
      <object class="GtkVBox" id="vbox1">
        <property name="visible">True</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkMenuBar" id="menubar1">
            <property name="visible">True</property>
            <child>
              <object class="GtkMenuItem" id="menuitem1">
                <property name="visible">True</property>
                <property name="label" translatable="yes">_File</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu1">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkImageMenuItem" id="file">
                        <property name="label">gtk-new</property>
                        <property name="visible">True</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                        <accelerator key="n" signal="activate" modifiers="GDK_CONTROL_MASK"/>
                        <signal name="activate" handler="new_workspace"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="Open Workspace">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">_Open Workspace...</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="open_workspace"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkSeparatorMenuItem" id="file_seperator1">
                        <property name="visible">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="Save">
                        <property name="visible">True</property>
                        <property name="sensitive">False</property>
                        <property name="label" translatable="yes">_Save</property>
                        <property name="use_underline">True</property>
                        <accelerator key="s" signal="activate" modifiers="GDK_CONTROL_MASK"/>
                        <signal name="activate" handler="save_workspace"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="Save Workspace">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Save Workspace _As...</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="save_workspace_as"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkSeparatorMenuItem" id="file_seperator2">
                        <property name="visible">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="Import...">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Import</property>
                        <property name="use_underline">True</property>
                        <child type="submenu">
                          <object class="GtkMenu" id="menu16">
                            <property name="visible">True</property>
                            <child>
                              <object class="GtkMenuItem" id="imagemenuitem4">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Data from File...</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="import_data"/>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="menuitem8">
                        <property name="label" translatable="yes">Export As</property>
                        <property name="visible">True</property>
                        <property name="use_stock">False</property>
                        <child type="submenu">
                          <object class="GtkMenu" id="menu7">
                            <property name="visible">True</property>
                            <child>
                              <object class="GtkMenuItem" id="menuitem9">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">LaTeX</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="export_latex"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="csv">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">CSV</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="export_csv"/>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child>
                      <object class="GtkSeparatorMenuItem" id="file_seperator3">
                        <property name="visible">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem5">
                        <property name="label">gtk-quit</property>
                        <property name="visible">True</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                        <signal name="activate" handler="destroy"/>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem" id="menuitem2">
                <property name="visible">True</property>
                <property name="label" translatable="yes">_Edit</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu2">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem6">
                        <property name="label">gtk-cut</property>
                        <property name="visible">True</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem7">
                        <property name="label">gtk-copy</property>
                        <property name="visible">True</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem8">
                        <property name="label">gtk-paste</property>
                        <property name="visible">True</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem9">
                        <property name="label">gtk-delete</property>
                        <property name="visible">True</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkSeparatorMenuItem" id="menuitem6">
                        <property name="visible">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="prefs">
                        <property name="label">gtk-preferences</property>
                        <property name="visible">True</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                        <signal name="activate" handler="preferences"/>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem" id="menuitem3">
                <property name="visible">True</property>
                <property name="label" translatable="yes">_View</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu18">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkMenuItem" id="Show Object Toolbar">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Show Object Toolbar</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="toggle_object_toolbar"/>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem" id="menuitem5">
                <property name="visible">True</property>
                <property name="label" translatable="yes">_Table</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu4">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkMenuItem" id="Add DataFrame">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">New Dataframe...</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="blankdata"/>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem" id="Data">
                <property name="visible">True</property>
                <property name="label" translatable="yes">_Data</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu5">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkMenuItem" id="Generate Random">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Generate Random</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="generate_random"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="Transform Data">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Transform Data</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="transform"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="Subset">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Subset</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="subset"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkSeparatorMenuItem" id="data_sep1">
                        <property name="visible">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="Sample">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Load Sample Dataset</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="sampledata"/>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem" id="menuitem10">
                <property name="visible">True</property>
                <property name="label" translatable="yes">_Analyze</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu8">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkMenuItem" id="Description">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Descriptions</property>
                        <property name="use_underline">True</property>
                        <child type="submenu">
                          <object class="GtkMenu" id="menu12">
                            <property name="visible">True</property>
                            <child>
                              <object class="GtkMenuItem" id="Summary">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Summary</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="summary"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Five Number Summary">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Five Number Summary</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="fivenum"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Mean">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Mean</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="mean"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Median">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Median</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="median"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Variance">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Variance</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="variance"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Standard Deviation">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Standard Deviation</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="sd"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Quantile">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Quantile</property>
                                <property name="use_underline">True</property>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="Frequency">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Frequency</property>
                        <property name="use_underline">True</property>
                        <child type="submenu">
                          <object class="GtkMenu" id="menu13">
                            <property name="visible">True</property>
                            <child>
                              <object class="GtkMenuItem" id="Frequency Table">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Frequency Table</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="freqtable"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Fisher's Exact Test">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Fisher's Exact Test</property>
                                <property name="use_underline">True</property>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="menuitem12">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Hypothesis Tests</property>
                        <property name="use_underline">True</property>
                        <child type="submenu">
                          <object class="GtkMenu" id="menu17">
                            <property name="visible">True</property>
                            <child>
                              <object class="GtkMenuItem" id="Student's T-Test">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Student's T-Test</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="ttest"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Chi-Square Test">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Chi-Square Test</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="chisq"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="McNemar's Chi-squared">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">McNemar's Chi-squared</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="mcnemar"/>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="menuitem14">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Correlation</property>
                        <property name="use_underline">True</property>
                        <child type="submenu">
                          <object class="GtkMenu" id="menu15">
                            <property name="visible">True</property>
                            <child>
                              <object class="GtkMenuItem" id="One Way ANOVA">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">One Way ANOVA</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="anova"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Correlation Tests">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Correlation Tests</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="cortest"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Correlation Coefficents">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Correlation Coefficents</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="cor"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Covariance">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Covariance</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="cov"/>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="Predictions">
                        <property name="label" translatable="yes">Predictions</property>
                        <property name="use_underline">True</property>
                        <child type="submenu">
                          <object class="GtkMenu" id="menu14">
                            <property name="visible">True</property>
                            <child>
                              <object class="GtkMenuItem" id="Linear Model">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Linear Model</property>
                                <property name="use_underline">True</property>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="menuitem15">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Regression</property>
                        <property name="use_underline">True</property>
                        <child type="submenu">
                          <object class="GtkMenu" id="menu9">
                            <property name="visible">True</property>
                            <child>
                              <object class="GtkMenuItem" id="menuitem16">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Linear</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="linear_regression"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="menuitem17">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Nonlinear</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="nonlinear_regression"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Polynomial Regression">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Polynomial Regression</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="polynomial_regression"/>
                              </object>
                            </child>
                            <child>
                              <object class="GtkMenuItem" id="Lowess">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">Local Regression</property>
                                <property name="use_underline">True</property>
                                <signal name="activate" handler="local_regression"/>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem" id="menuitem7">
                <property name="visible">True</property>
                <property name="label" translatable="yes">_Plot</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu6">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkMenuItem" id="menuitem21">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Scatter</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="scatterplot"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="Matrix">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Multiple Scatter</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="mscatter"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="menuitem18">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Bar Plot</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="barplot"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="menuitem13">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Box Plot</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="boxplot"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="menuitem19">
                        <property name="label" translatable="yes">Biplot</property>
                        <property name="use_underline">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="hist">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Histogram</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="histogram"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="menuitem20">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Q-Q</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="qqplot"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="menuitemabc">
                        <property name="label" translatable="yes">Cluster</property>
                        <property name="use_underline">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="menuitem11">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Pie</property>
                        <property name="use_underline">True</property>
                        <signal name="activate" handler="pieplot"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="Stem">
                        <property name="label" translatable="yes">Stem</property>
                        <property name="use_underline">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkSeparatorMenuItem" id="menuitem27">
                        <property name="visible">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="ggplot_menu">
                        <property name="visible">True</property>
                        <property name="sensitive">False</property>
                        <property name="label" translatable="yes">GGPlot</property>
                        <property name="use_underline">True</property>
                        <child type="submenu">
                          <object class="GtkMenu" id="menu10">
                            <property name="visible">True</property>
                            <child>
                              <object class="GtkMenuItem" id="menuitem23">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">TODO</property>
                                <property name="use_underline">True</property>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child>
                      <object class="GtkMenuItem" id="lattice_menu">
                        <property name="visible">True</property>
                        <property name="sensitive">False</property>
                        <property name="label" translatable="yes">Lattice</property>
                        <property name="use_underline">True</property>
                        <child type="submenu">
                          <object class="GtkMenu" id="menu11">
                            <property name="visible">True</property>
                            <child>
                              <object class="GtkMenuItem" id="menuitem25">
                                <property name="visible">True</property>
                                <property name="label" translatable="yes">TODO</property>
                                <property name="use_underline">True</property>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem" id="menuitem4">
                <property name="visible">True</property>
                <property name="label" translatable="yes">_Help</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu3">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem10">
                        <property name="label">gtk-about</property>
                        <property name="visible">True</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                        <signal name="activate" handler="about"/>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkToolbar" id="main_toolbar">
            <property name="visible">True</property>
            <property name="border_width">1</property>
            <property name="toolbar_style">icons</property>
            <child>
              <object class="GtkToolButton" id="toolbutton1">
                <property name="width_request">16</property>
                <property name="height_request">16</property>
                <property name="visible">True</property>
                <property name="use_underline">True</property>
                <property name="icon_name">document-open</property>
                <signal name="clicked" handler="import_data"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="toolbutton5">
                <property name="width_request">16</property>
                <property name="height_request">16</property>
                <property name="visible">True</property>
                <property name="tooltip_text" translatable="yes">Quick Calculate</property>
                <property name="use_underline">True</property>
                <property name="icon_widget">calculatoricon</property>
                <signal name="clicked" handler="summary"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkSeparatorToolItem" id="toolbutton3">
                <property name="visible">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="scatterbutton">
                <property name="visible">True</property>
                <property name="tooltip_text" translatable="yes">Scatter Plot</property>
                <property name="use_underline">True</property>
                <property name="icon_widget">scattericon</property>
                <signal name="clicked" handler="scatterplot"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="histbutton">
                <property name="visible">True</property>
                <property name="use_underline">True</property>
                <property name="icon_widget">histicon</property>
                <signal name="clicked" handler="histogram"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="piebutton">
                <property name="visible">True</property>
                <property name="tooltip_text" translatable="yes">Pie Plot</property>
                <property name="use_underline">True</property>
                <property name="icon_widget">pieicon</property>
                <signal name="clicked" handler="pieplot"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="matplotubbton">
                <property name="visible">True</property>
                <property name="tooltip_text" translatable="yes">Matrix Scatter Plot</property>
                <property name="use_underline">True</property>
                <property name="icon_widget">matploticon</property>
                <signal name="clicked" handler="mscatter"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="boxplotbutton">
                <property name="width_request">16</property>
                <property name="height_request">16</property>
                <property name="visible">True</property>
                <property name="tooltip_text" translatable="yes">Box Plot</property>
                <property name="use_underline">True</property>
                <property name="icon_widget">boxplot</property>
                <signal name="clicked" handler="boxplot"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="toolbutton6">
                <property name="visible">True</property>
                <property name="tooltip_text" translatable="yes">Bar Plot</property>
                <property name="use_underline">True</property>
                <property name="icon_widget">barploticon</property>
                <signal name="clicked" handler="barplot"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkSeparatorToolItem" id="toolbutton2">
                <property name="visible">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="nonlinregbutton">
                <property name="visible">True</property>
                <property name="use_underline">True</property>
                <property name="icon_widget">linearregicon</property>
                <signal name="clicked" handler="linear_regression"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="linregbutton">
                <property name="visible">True</property>
                <property name="use_underline">True</property>
                <property name="icon_widget">nonlingregicon</property>
                <signal name="clicked" handler="nonlinear_regression"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkHBox" id="hbox1">
            <property name="visible">True</property>
            <child>
              <object class="GtkHPaned" id="main_pane">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <child>
                  <object class="GtkNotebook" id="main_tabview">
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <child>
                      <object class="GtkScrolledWindow" id="dataview_scroller">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="hscrollbar_policy">automatic</property>
                        <property name="vscrollbar_policy">automatic</property>
                        <child>
                          <object class="GtkViewport" id="viewport1">
                            <property name="visible">True</property>
                            <property name="resize_mode">queue</property>
                            <child>
                              <object class="GtkHBox" id="hbox2">
                                <property name="visible">True</property>
                                <child>
                                  <object class="GtkTreeView" id="rownames">
                                    <property name="visible">True</property>
                                    <property name="headers_clickable">False</property>
                                    <property name="rules_hint">True</property>
                                    <property name="enable_search">False</property>
                                    <property name="enable_grid_lines">both</property>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="position">0</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkVSeparator" id="vseparator1">
                                    <property name="visible">True</property>
                                    <property name="orientation">vertical</property>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="position">1</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkTreeView" id="dataview">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="rules_hint">True</property>
                                    <property name="enable_search">False</property>
                                    <property name="enable_grid_lines">both</property>
                                    <signal name="button_press_event" handler="col_contextmenu"/>
                                  </object>
                                  <packing>
                                    <property name="position">2</property>
                                  </packing>
                                </child>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                      <packing>
                        <property name="reorderable">True</property>
                      </packing>
                    </child>
                    <child type="tab">
                      <object class="GtkLabel" id="data_label">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Data</property>
                      </object>
                      <packing>
                        <property name="tab_fill">False</property>
                        <property name="reorderable">True</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkScrolledWindow" id="scrolledwindow1">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="hscrollbar_policy">automatic</property>
                        <property name="vscrollbar_policy">automatic</property>
                        <child>
                          <object class="GtkTextView" id="summaryview">
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="editable">False</property>
                          </object>
                        </child>
                      </object>
                      <packing>
                        <property name="position">1</property>
                        <property name="reorderable">True</property>
                      </packing>
                    </child>
                    <child type="tab">
                      <object class="GtkLabel" id="summary_label">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Summary</property>
                      </object>
                      <packing>
                        <property name="position">1</property>
                        <property name="tab_fill">False</property>
                        <property name="reorderable">True</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkVBox" id="console_tab">
                        <property name="visible">True</property>
                        <property name="orientation">vertical</property>
                        <child>
                          <object class="GtkScrolledWindow" id="consoleview_scroll">
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="hscrollbar_policy">automatic</property>
                            <property name="vscrollbar_policy">automatic</property>
                            <child>
                              <object class="GtkTextView" id="consoleview">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="editable">False</property>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="position">0</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkHBox" id="execution_vbox">
                            <property name="visible">True</property>
                            <property name="border_width">4</property>
                            <property name="spacing">2</property>
                            <child>
                              <object class="GtkEntry" id="command_entry">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="has_frame">False</property>
                                <property name="invisible_char">&#x25CF;</property>
                                <property name="activates_default">True</property>
                                <property name="primary_icon_stock">gtk-yes</property>
                                <property name="primary_icon_sensitive">True</property>
                                <property name="primary_icon_tooltip_text">No Error</property>
                                <signal name="activate" handler="execute_command"/>
                              </object>
                              <packing>
                                <property name="position">0</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkButton" id="execute_command">
                                <property name="label" translatable="yes">Execute</property>
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="receives_default">True</property>
                                <accelerator key="Return" signal="clicked"/>
                                <signal name="clicked" handler="execute_command"/>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="position">1</property>
                              </packing>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">False</property>
                            <property name="position">1</property>
                          </packing>
                        </child>
                      </object>
                      <packing>
                        <property name="position">2</property>
                        <property name="reorderable">True</property>
                      </packing>
                    </child>
                    <child type="tab">
                      <object class="GtkLabel" id="console_label">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">Console</property>
                      </object>
                      <packing>
                        <property name="position">2</property>
                        <property name="tab_fill">False</property>
                        <property name="reorderable">True</property>
                      </packing>
                    </child>
                  </object>
                  <packing>
                    <property name="resize">True</property>
                    <property name="shrink">True</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkViewport" id="right_dock">
                    <property name="visible">True</property>
                    <property name="resize_mode">queue</property>
                    <child>
                      <placeholder/>
                    </child>
                  </object>
                  <packing>
                    <property name="resize">True</property>
                    <property name="shrink">False</property>
                  </packing>
                </child>
              </object>
              <packing>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="position">2</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
  <object class="GtkMenu" id="colmenu">
    <property name="visible">True</property>
    <property name="tearoff_title">Column Operations</property>
    <child>
      <object class="GtkMenuItem" id="Column Operations">
        <property name="visible">True</property>
        <property name="sensitive">False</property>
        <property name="label" translatable="yes">Column Operations</property>
        <property name="use_underline">True</property>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem22">
        <property name="visible">True</property>
        <property name="label" translatable="yes">Mean</property>
        <property name="use_underline">True</property>
        <signal name="activate" handler="context_mean"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem44">
        <property name="visible">True</property>
        <property name="label" translatable="yes">Median</property>
        <property name="use_underline">True</property>
        <signal name="activate" handler="context_median"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem33">
        <property name="visible">True</property>
        <property name="label" translatable="yes">Standard Deviation</property>
        <property name="use_underline">True</property>
        <signal name="activate" handler="context_sd"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem111">
        <property name="visible">True</property>
        <property name="label" translatable="yes">Variance</property>
        <property name="use_underline">True</property>
        <signal name="activate" handler="context_variance"/>
      </object>
    </child>
    <child>
      <object class="GtkImageMenuItem" id="menuitem77">
        <property name="label" translatable="yes">Delete Row</property>
        <property name="visible">True</property>
        <property name="use_stock">False</property>
        <signal name="activate" handler="context_delrow"/>
      </object>
    </child>
    <child>
      <object class="GtkImageMenuItem" id="menuitem68">
        <property name="label" translatable="yes">Delete Column</property>
        <property name="visible">True</property>
        <property name="use_stock">False</property>
        <signal name="activate" handler="context_delcol"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="Rename">
        <property name="visible">True</property>
        <property name="label" translatable="yes">Rename Column</property>
        <property name="use_underline">True</property>
        <signal name="activate" handler="context_rename"/>
      </object>
    </child>
  </object>
  <object class="GtkWindow" id="textoutput">
    <property name="width_request">300</property>
    <property name="height_request">300</property>
    <property name="title" translatable="yes">Output</property>
    <property name="destroy_with_parent">True</property>
    <child>
      <object class="GtkVBox" id="vbox1a">
        <property name="visible">True</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkScrolledWindow" id="scrolledwindow1a">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="hscrollbar_policy">automatic</property>
            <property name="vscrollbar_policy">automatic</property>
            <child>
              <object class="GtkTextView" id="output">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="editable">False</property>
                <property name="cursor_visible">False</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkHBox" id="hbox1a">
            <property name="visible">True</property>
            <child>
              <placeholder/>
            </child>
            <child>
              <object class="GtkButton" id="close_textoutput">
                <property name="label">gtk-ok</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_stock">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="pack_type">end</property>
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
  </object>
  <object class="GtkAssistant" id="random">
    <property name="border_width">12</property>
    <property name="modal">True</property>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <object class="GtkTable" id="distributions">
        <property name="visible">True</property>
        <property name="n_rows">4</property>
        <child>
          <object class="GtkRadioButton" id="radiobutton3">
            <property name="label" translatable="yes">Normal Distribution</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">False</property>
            <property name="active">True</property>
            <property name="draw_indicator">True</property>
            <property name="group">radiobutton2</property>
          </object>
          <packing>
            <property name="top_attach">2</property>
            <property name="bottom_attach">3</property>
          </packing>
        </child>
        <child>
          <object class="GtkRadioButton" id="radiobutton2">
            <property name="label" translatable="yes">Random Floats</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">False</property>
            <property name="active">True</property>
            <property name="draw_indicator">True</property>
          </object>
          <packing>
            <property name="top_attach">1</property>
            <property name="bottom_attach">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkRadioButton" id="radiobutton1">
            <property name="label" translatable="yes">Random Integers</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">False</property>
            <property name="active">True</property>
            <property name="draw_indicator">True</property>
            <property name="group">radiobutton2</property>
          </object>
        </child>
        <child>
          <placeholder/>
        </child>
      </object>
      <packing>
        <property name="page_type">intro</property>
        <property name="title" translatable="yes">Distribution</property>
      </packing>
    </child>
    <child>
      <object class="GtkTable" id="generation_parameters">
        <property name="visible">True</property>
        <property name="n_rows">3</property>
        <property name="n_columns">3</property>
        <child>
          <object class="GtkLabel" id="rows">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Rows to Generate</property>
          </object>
          <packing>
            <property name="top_attach">1</property>
            <property name="bottom_attach">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkLabel" id="cols">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Columns to Generate</property>
          </object>
        </child>
        <child>
          <object class="GtkSpinButton" id="gen_columns1">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="invisible_char">&#x25CF;</property>
            <property name="climb_rate">1</property>
            <property name="snap_to_ticks">True</property>
            <property name="numeric">True</property>
          </object>
          <packing>
            <property name="left_attach">1</property>
            <property name="right_attach">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkSpinButton" id="gen_columns">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="invisible_char">&#x25CF;</property>
            <property name="climb_rate">1</property>
            <property name="snap_to_ticks">True</property>
            <property name="numeric">True</property>
          </object>
          <packing>
            <property name="left_attach">1</property>
            <property name="right_attach">2</property>
            <property name="top_attach">1</property>
            <property name="bottom_attach">2</property>
            <property name="y_options">GTK_FILL</property>
          </packing>
        </child>
        <child>
          <placeholder/>
        </child>
        <child>
          <placeholder/>
        </child>
        <child>
          <placeholder/>
        </child>
        <child>
          <placeholder/>
        </child>
        <child>
          <placeholder/>
        </child>
      </object>
      <packing>
        <property name="title" translatable="yes">Parameters</property>
      </packing>
    </child>
  </object>
  <object class="GtkImage" id="scattericon">
    <property name="visible">True</property>
    <property name="pixbuf">icons/scatter.png</property>
  </object>
  <object class="GtkImage" id="histicon">
    <property name="visible">True</property>
    <property name="tooltip_text" translatable="yes">Histogram</property>
    <property name="pixbuf">icons/histogram.svg</property>
  </object>
  <object class="GtkImage" id="pieicon">
    <property name="visible">True</property>
    <property name="pixbuf">icons/pie.png</property>
  </object>
  <object class="GtkImage" id="matploticon">
    <property name="visible">True</property>
    <property name="xalign">0.50999999046325684</property>
    <property name="pixbuf">icons/matplot.svg</property>
  </object>
  <object class="GtkImage" id="boxplot">
    <property name="visible">True</property>
    <property name="pixbuf">icons/boxplot.svg</property>
  </object>
  <object class="GtkImage" id="barploticon">
    <property name="visible">True</property>
    <property name="pixbuf">icons/bar.png</property>
  </object>
  <object class="GtkImage" id="linearregicon">
    <property name="visible">True</property>
    <property name="pixbuf">icons/linear-regression.svg</property>
  </object>
  <object class="GtkImage" id="nonlingregicon">
    <property name="visible">True</property>
    <property name="pixbuf">icons/nonlinear-regression.svg</property>
  </object>
  <object class="GtkImage" id="calculatoricon">
    <property name="visible">True</property>
    <property name="tooltip_text" translatable="yes">
</property>
    <property name="pixbuf">icons/calculator.png</property>
  </object>
  <object class="GtkVBox" id="object_sidebar">
    <property name="visible">True</property>
    <property name="orientation">vertical</property>
    <child>
      <object class="GtkTreeView" id="objectview">
        <property name="visible">True</property>
        <property name="can_focus">True</property>
        <property name="rules_hint">True</property>
        <signal name="button_press_event" handler="selectobject"/>
      </object>
      <packing>
        <property name="position">0</property>
      </packing>
    </child>
    <child>
      <object class="GtkToolbar" id="object_toolbar">
        <property name="visible">True</property>
        <property name="toolbar_style">icons</property>
        <property name="show_arrow">False</property>
        <property name="icon_size">1</property>
        <property name="icon_size_set">True</property>
        <child>
          <object class="GtkToolButton" id="toolbutton4">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Add</property>
            <property name="use_underline">True</property>
            <property name="stock_id">gtk-add</property>
            <signal name="clicked" handler="blankdata"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="homogeneous">True</property>
          </packing>
        </child>
        <child>
          <object class="GtkToolButton" id="duplicate_button">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Duplicate</property>
            <property name="use_underline">True</property>
            <property name="stock_id">gtk-copy</property>
            <signal name="clicked" handler="duplicate_r_object"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="homogeneous">True</property>
          </packing>
        </child>
        <child>
          <object class="GtkToolButton" id="rename_button">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Rename</property>
            <property name="use_underline">True</property>
            <property name="stock_id">gtk-edit</property>
            <signal name="clicked" handler="rename_r_object"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="homogeneous">True</property>
          </packing>
        </child>
        <child>
          <object class="GtkToolButton" id="delete_button">
            <property name="visible">True</property>
            <property name="label" translatable="yes">Delete</property>
            <property name="use_underline">True</property>
            <property name="stock_id">gtk-delete</property>
            <signal name="clicked" handler="delete_r_object"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="homogeneous">True</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="expand">False</property>
        <property name="pack_type">end</property>
        <property name="position">1</property>
      </packing>
    </child>
  </object>
</interface>
