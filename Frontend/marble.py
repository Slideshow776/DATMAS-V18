from PyQt4.QtGui import *
from PyKDE4.marble import *
import sys
 
def main():
  # Initialize QApplication
  app = QApplication(sys.argv)
 
  # Create a Marble QWidget
  m = Marble.MarbleWidget()
 
  # Load the OpenStreeMap map
  m.setMapThemeId("earth/openstreetmap/openstreetmap.dgml")
 
  # Show the window
  m.show()
 
  # Run the app
  app.exec_()
 
main()