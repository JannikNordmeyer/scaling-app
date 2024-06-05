#+property: header-args :wrap src text
#+property: header-args:text :eval never

* Scaling App

The Scaling App provides functionality for manipulating formal contexts and performing conceptual scaling on many valued contexts.
The application supports drawing concept lattices, computing concepts, implications and implication rules, as well as attribute exploration.

** Installation:
This app requires Python 3.12:
https://www.python.org/downloads/release/python-3120/

The following packages are required to run the scaling app:

#+begin_src sh :eval never
cx-Freeze 7.0.0
cx-Logging 3.2.0
cycler 0.11.0
fonttools 4.34.4
importlib-metadata 4.12.0
kiwisolver 1.4.5
lief 0.14.1
matplotlib 3.8.4
networkx 2.8.5
numpy 1.26.4
packaging 21.3
pandas 2.2.2
Pillow 10.3.0
pyparsing 3.0.9
python-dateutil 2.8.2
pytz 2022.1
scipy 1.13.0
seaborn 0.12.2
six==1.16.0
wxPython 4.2.1
zipp 3.8.1
requests 2.27.1
cx_Freeze 7.0.0
#+end_src

To install all necessary packages run:
#+begin_src sh :eval never
pip3 install -r requirements.txt
#+end_src
You can then start the app by running:
#+begin_src sh :eval never
py main.py
#+end_src
(Depending on your python installations and platform Python 3.12 may have to be called using ~python~ or ~python3~ instead of ~py~.)

In order to access all functions of the app, ~conexp-clj~ needs to be run.
https://github.com/tomhanika/conexp-clj
In order to execute conexp-clj you need to install Leiningen:
https://leiningen.org/
The conexp-clj API can be accessed from any address, but the apps tries to find the API at localhost by default.
To host the API under localhost, navigate to the repository and execute:
#+begin_src sh :eval never
lein run -a
#+end_src


** Formal Contexts:
The formal context can be edited under the ~Formal Context~ tab, which is selected by default.
The incidence of the formal contex can be directly manipulated by clicking the cells. Objects and attributes can be edited by right-clicking their labels.
The concept lattice can be drawn via right-clicking the cells of the context, or by using the button on the top left panel.

** Attribute Exploration:
Attribute Exploration builds a context based on expert knowledge about a subject.
Attribute exploration can be accessed via the menu bar at the top of the window. You will be prompted to enter a set of starting attributes (comma separated).
The algorithm will they identify possible implications between the attributes. You will be asked to either confirm these implications,
or provide one or more counterexamples in form of an object whose attributes contradict the implication. You may cancel the exploration at any time.
The current exploration state will be stored and the current context will be displayed in the corresponding tab. You may continue the exploration
via menu bar at the top of the window.

** Conceptual Scaling:
Switching to the ~Conceptual Scaling~ tab at the top of the screen.
The many valued context can be manipulated is the same way as the formal context.
You can load a many valued context from a CSV file by selecting Data->Load Data from the top menu bar.
By right-clicking the attribute labels you can set the level of measurement which affects the scales you have access to. 
A scaling for the attribute can be selected from the same menu. Scaling an attribute will add a neu tab to where the scale can be manipulated. 
The tab labeled ~Scaled Context~ displays the many valued context with all scales applied. This context, as well as the individual scales can be dawn as concept lattices
in the same way as described earlier.

Selecting ~Display Statistics~ from the attribute menu opens a tab at the bottom right that can display the distribution of the values in various modes.
This tab allows for the definition of a custom order on the values under the ~Custom Order~ tab. In the ~Expanded Histogram~ tab,
the values can be distributed into interval. This only works if the ordering is set to "Numeric" in the dropdown menu below.


** General Functions:
The bottom right displays tabs for "Concepts", "Implications" and "Rules". Those tabs can compute the concepts, implications and implication rules
for either the formal context, or the scaled many valued context, depending on which tab is selected.
