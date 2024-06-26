# Gran Turismo 7 Track Visualizer | UDP Stream -> CSV Parser -> Plotly

gt7_udp_csv_parser is used to parse UDP packets and output a CSV. All other programs with "visualization" in the title are for plotting the points, forming a track map using Plotly. Any CSVs placed in the "data" folder will be read by the programs and be plotted.

## Quick Start

1. Clone this repository `git clone https://github.com/macmanley/gt7-track-visualizer.git`
2. Use python to run the scripts. Sample track and session data is included in the "tracks" folder. Simply drag any CSVs you want visualized into the "data" folder, then run one of the visualization scripts.

Example: `python .\speed_heatmap_visualization.py`

## Track IDs

| ID   | Track Name                                                  |
|------|-------------------------------------------------------------|
| 4    | Daytona Tri-Oval                                            |
| 10   | Suzuka Circuit                                              |
| 11   | High Speed Ring                                             |
| 16   | Fuji International Speedway                                 |
| 41   | WeatherTech Raceway Laguna Seca                             |
| 51   | Deep Forest Raceway                                         |
| 95   | Nurburgring Nordschleife                                    |
| 116  | Mount Panorama Motor Racing Circuit                         |
| 119  | Brands Hatch Grand Prix Circuit                             |
| 122  | Willow Springs International Raceway: Big Willow            |
| 123  | Willow Springs International Raceway: Streets of Willow Springs |
| 125  | Willow Springs International Raceway: Horse Thief Mile      |
| 152  | Autodromo de Interlagos                                     |
| 154  | Goodwood Motor Circuit                                      |
| 346  | Brands Hatch Indy Circuit                                   |
| 347  | Nurburgring Nordschleife Tourist Layout                     |
| 348  | Nurburgring 24h                                             |
| 349  | Nurburgring GP                                              |
| 351  | Tokyo Expressway - Central Clockwise                        |
| 353  | Fishermans Ranch                                            |
| 354  | Northern Isle Speedway                                      |
| 356  | Blue Moon Bay Speedway                                      |
| 357  | BB Raceway                                                  |
| 358  | Alsace - Village                                            |
| 361  | Tokyo Expressway - East Clockwise                           |
| 362  | Tokyo Expressway - South Clockwise                          |
| 363  | Dragon Trail - Seaside                                      |
| 365  | Autodrome Lago Maggiore - Full Course                       |
| 372  | Colorado Springs - Lake                                     |
| 376  | Kyoto Driving Park - Yamagiwa                               |
| 439  | Alsace - Village Reverse                                    |
| 440  | Kyoto Driving Park - Miyabi                                 |
| 442  | Suzuka Circuit East Course                                  |
| 443  | Fishermans Ranch Reverse                                    |
| 444  | BB Raceway Reverse                                          |
| 449  | Blue Moon Bay Speedway Reverse                              |
| 450  | Tokyo Expressway - Central Counterclockwise                 |
| 451  | Tokyo Expressway - East Counterclockwise                    |
| 452  | Willow Springs International Raceway: Horse Thief Mile Reverse |
| 453  | Sardegna - Windmills                                        |
| 454  | 24 Heures du Mans Racing Circuit                            |
| 462  | Circuit de Spa-Francorchamps                                |
| 469  | Autodromo Nazionale Monza                                   |
| 470  | Red Bull Ring                                               |
| 471  | Tsukuba Circuit                                             |
| 598  | Willow Springs International Raceway: Streets of Willow Springs Reverse |
| 599  | Sardegna - Windmills Reverse                                |
| 600  | Colorado Springs - Lake Reverse                             |
| 601  | Dragon Trail - Seaside Reverse                              |
| 602  | Autodrome Lago Maggiore - Full Course Reverse               |
| 613  | Kyoto Driving Park - Yamagiwa Reverse                       |
| 742  | Autodromo Nazionale Monza No Chicane                        |
| 747  | Deep Forest Raceway Reverse                                 |
| 776  | Kyoto Driving Park - Yamagiwa+Miyabi                        |
| 777  | Kyoto Driving Park - Yamagiwa+Miyabi Reverse                |
| 790  | Autodrome Lago Maggiore - East End Reverse                  |
| 791  | Autodrome Lago Maggiore - Centre Reverse                    |
| 792  | Autodrome Lago Maggiore - West End                          |
| 793  | Autodrome Lago Maggiore - Centre                            |
| 794  | Autodrome Lago Maggiore - West End Reverse                  |
| 795  | Autodrome Lago Maggiore - East End                          |
| 819  | Blue Moon Bay Speedway - Infield B                          |
| 820  | Blue Moon Bay Speedway - Infield A                          |
| 822  | Blue Moon Bay Speedway - Infield A Reverse                  |
| 823  | Blue Moon Bay Speedway - Infield B Reverse                  |
| 825  | Circuit de Sainte-Croix - A                                 |
| 826  | Circuit de Sainte-Croix - A Reverse                         |
| 827  | Circuit de Sainte-Croix - B                                 |
| 828  | Circuit de Sainte-Croix - B Reverse                         |
| 829  | Circuit de Sainte-Croix - C                                 |
| 830  | Circuit de Sainte-Croix - C Reverse                         |
| 837  | Fuji International Speedway (Short)                         |
| 838  | Sardegna - Road Track - C Reverse                           |
| 839  | Sardegna - Road Track - B Reverse                           |
| 841  | Sardegna - Road Track - B                                   |
| 843  | Sardegna - Road Track - C                                   |
| 846  | Red Bull Ring Short Track                                   |
| 847  | Dragon Trail - Gardens                                      |
| 853  | Dragon Trail - Gardens Reverse                              |
| 854  | 24 Heures du Mans Racing Circuit No Chicane                 |
| 874  | Circuit de Barcelona-Catalunya Grand Prix Layout            |
| 896  | Autopolis International Racing Course                       |
| 898  | Autopolis International Racing Course - Short Course        |
| 915  | Tokyo Expressway - South Counterclockwise                   |
| 921  | Sardegna - Road Track - A                                   |
| 922  | Sardegna - Road Track - A Reverse                           |
| 1024 | Trial Mountain Circuit                                      |
| 1034 | Trial Mountain Circuit - Reverse                            |
| 1069 | High Speed Ring Reverse                                     |
| 1163 | Daytona Road Course                                         |
| 1224 | Alsace - Test Course                                        |
| 1225 | Autodrome Lago Maggiore - WestAlsace - Test Course Reverse  |
| 1226 | Autodrome Lago Maggiore - East                              |
| 1231 | Autodrome Lago Maggiore - East Reverse                      |
| 1232 | Autodrome Lago Maggiore - West                              |
| 1233 | Autodrome Lago Maggiore - West Reverse                      |
| 1260 | Special Stage Route X                                       |
| 1261 | Special Stage Route X 400                                   |
| 1262 | Special Stage Route X 1000                                  |
| 1269 | Spa 24h Layout                                              |
| 1240 | Watkins Glen Long Course                                    |
| 1264 | Watkins Glen Short Course                                   |
| 1249 | Circuit de Barcelona-Catalunya GP Layout No Chicane         |
| 1250 | Circuit de Barcelona-Catalunya National                     |
| 1265 | Circuit de Barcelona-Catalunya Rallycross                   |

> All sample CSVs available in the "data" folder were driven using the Mercedes AMG GT3 '20.

Please also check out my other GT7 Library for the ESP32/ESP8266 microcontrollers [here](https://github.com/MacManley/gt7-udp)
