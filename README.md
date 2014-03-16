atpg-PODEM
==========

This Automatic Test Pattern Generation (ATPG) program takes in a combinational circuit defined as a graph and a single stuck-at-fault expressed as either D or D(bar), and runs the 5-valued PODEM algorithm to determine whether the error can be propagated to the output for an input test vector, and also displays the state of the graph (including input test vector) for error propagation.  

The inputs are entred by hand within program itself, to run sample example, do ./atpg_combinational_5valued.py
