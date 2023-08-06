# coding: utf-8

desc={"ref": {"12(1)": "C. Lobban, J. L. Finney, W. F. Kuhs, Nature, 1998, DOI:10.1038/34622.",
              "12(2)": 'Koza, M M et al. "Ice XII in Its Second Regime of Metastability." Physical Review Letters 84.18 (2000): 4112-4115.'},
      "usage": "No options available.",
      "brief": "Ice XII."
      }

bondlen = 3      #bond threshold	 

cell = """
8.2816 8.2816 8.0722
"""

density=1.4397

waters="""
0.75 0.13356 0.1875
0.75 0.13536 0.6875
0.86464 0.75 0.3125
0.86464 0.75 0.8125
0.13536 0.25 0.3125
0.13536 0.25 0.8125
0.5 0 0.375
0.5 0 0.875
0.25 0.86464 0.1875
0.25 0.86464 0.6875
0 0.5 0.125
0 0.5 0.625
0.5 0.5 0.25
0.5 0.5 0.75
0 0 0
0 0 0.5
0.25 0.63536 0.4375
0.25 0.63536 0.9375
0.36464 0.25 0.0625
0.36464 0.25 0.5625
0.75 0.36564 0.4375
0.75 0.36564 0.9375
0.63536 0.75 0.0625
0.63536 0.75 0.5625
"""

coord="relative"

from genice.cell import cellvectors
cell = cellvectors(a=8.2816,
                   b=8.2816,
                   c=8.0722)
