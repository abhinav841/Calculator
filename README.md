# Calculator

We aim to perform calculation with 100% accuracy.

Every calculator that doesn't simplify the expression has some inaccuracy.
Simply because some intermediate values in calculation require infinite precision when stored in decimal form.

For example, **√5×√5** equals exactly **5** but how a typical calculator evaluates it is:

           √5 : 2.23606797749979
       So, √5×√5 = 2.23606797749979×2.23606797749979
                 = 5.000000000000001

Although it gets rounded off and what you see is **5**, you can check it as:
           
1. (√5×√5 - 5) doesn't give 0 in Microsoft Calculator
2. 1/(√11×√11 - 11) results in calculation timeout instead of zero division error in Realme Calculator
3. 1/(((√2)^(√2))^(√2)-2) doesn't give ComplexInfinity Error in MathDa as it gives in a 1÷0 case

This was only to give you an idea of what we are aiming at.

Inaccuracy in rational decimals is easy to get rid of by handling them as fractions. The real quest is handling irrationals!
