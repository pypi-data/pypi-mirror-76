.. :changelog:

Release History
===============
1.3.10 (2020-08-08)
-------------------
* Reformat code using Black instead of Autopep8

1.3.9 (2020-08-04)
------------------
* Migrate from PyCharm to VSCode
* Code refactoring and cleanup using Autopep8 and Pylint
* Add undocumented ecobee objects (Energy & TimeOfUse)

1.3.8 (2020-08-01)
------------------
* Add fan_speed to Event object

1.3.7 (2020-07-31)
------------------
* Handle KeyError exception in case of new property added by ecobee

1.3.6 (2020-07-31)
------------------
* Add fan_speed to Settings object

1.3.5 (2020-04-03)
------------------
* Code refactoring and cleanup

1.3.0 (2020-04-02)
------------------
* Uplift the implementation to include all update to the ecobee API since mid 2017

1.2.1 (2017-06-01)
------------------
* Internal __slots__ improvements

1.2.0 (2017-05-31)
------------------
* Internal refactoring of EcobeeObject and EcobeeResponse


1.1.1 (2017-05-31)
------------------
* Miscellaneous minor internal changes to facilitate the automatic generation of PlantUML Class Diagrams


1.1.0 (2017-05-24)
------------------
* Added ecobee API operations that are only accessible by EMS and Utility accounts


1.0.0 (2017-05-12)
------------------
* First public release supporting all ecobee API operations except those that are only accessible by EMS and Utility accounts
