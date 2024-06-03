Scaling App

The Scaling App provides functionality for manipulating formal contexts and performing conceptual scaling on many valued contexts.
The application supports drawing concept lattices, computing concepts, implications and implication rules, as well as attribute exploration.

Installation:
This app requires Python 3.12:
https://www.python.org/downloads/release/python-3120/
To install all necessary packages run "pip3 install -r requirements.txt". 
You can then start the app by running "py main.py".
(Depending on your python installations and platform Python 3.12 may have to be called using "python" or "python3" instead of "py".)

In order to access all functions of the app, "conexp-clj" needs to be run. 
https://github.com/tomhanika/conexp-clj
In order to execute conexp-clj you need to install Leiningen:
https://leiningen.org/
The conexp-clj API can be accessed from any address, but the apps tries to find the API at localhost by default.
To host the API under localhost, navigate to the repository and execute "lein run -a".



Formal Contexts:
The formal context can be edited under the "Formal Context" tab, which is selected by default.
The incidence of the formal contex can be directly manipulated by clicking the cells. Objects and attributes can be edited by right-clicking their labels.
The concept lattice can be drawn via right-clicking the cells of the context, or by using the button on the top left panel.

Attribute Exploration:
Attribute Exploration builds a context based on expert knowledge about a subject.
Attribute exploration can be accessed via the menu bar at the top of the window. You will be prompted to enter a set of starting attributes (comma separated).
The algorithm will they identify possible implications between the object. You will be asked to either confirm these implications,
or provide a counterexample in form of an object whose attributes contradict the implication.

Conceptual Scaling:
Switching to the "Conceptual Scaling" tab at the top of the screen.
The many valued context can be manipulated is the same way as the formal context.
You can load a many valued context from a CSV file by selecting Data->Load Data from the top menu bar.
By right-clicking the attribute labels you can set the level of measurement which affects the scales you have access to. 
A scaling for the attribute can be selected from the same menu. Scaling an attribute will add a neu tab to where the scale can be manipulated. 
The tab labeled "Scaled Context" displays the many valued context with all scales applied. This context, as well as the individual scales can be dawn as concept lattices
in the same way as described earlier.

Selecting "Display Statistics" from the attribute menu opens a tab at the bottom right that can display the distribution of the values in various modes.
This tab allows for the definition of a custom order on the values under the "Custom Order" tab. In the "Expanded Histogram" tab,
the values can be distributed into interval. This only works if the ordering is set to "Numeric" in the dropdown menu below.


General Functions:
The bottom right displays tabs for "Concepts", "Implications" and "Rules". Those tabs can compute the concepts, implications and implication rules
for either the formal context, or the scaled many valued context, depending on which tab is selected.
