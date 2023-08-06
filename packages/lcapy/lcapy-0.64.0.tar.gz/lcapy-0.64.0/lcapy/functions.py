"""This module provides functions.

Copyright 2014--2020 Michael Hayes, UCECE
"""


import sympy as sym

class Function(object):

    def __init__(self, arg):
        self.expr = arg
    
    def __call__(self, *args):

        cls = args[0].__class__

        # Unwrap expressions
        tweak_args = list(args)
        for m, arg in enumerate(args):
            if isinstance(arg, (Expr, Function)):
                tweak_args[m] = arg.expr

        result = self.expr(*tweak_args)

        if isinstance(args[0], Expr):
            result = cls(result)

        if False:
            for m, arg in enumerate(args[1:]):
                if isinstance(arg, (Expr, Function)):
                    # Need to avoid substituting constants
                    result = result.subs(tweak_args[m], arg)

        return result

    
class Log10(Function):

    # TODO, figure out how to print as log10(x) rather than
    # the expansion log(x) / log(10).  This will require
    # deferment of the expansion.
    
    def __call__(self, arg):
        return super(Log10, self).__call__(arg, 10)

   
conjugate = Function(sym.conjugate)

sqrt = Function(sym.sqrt)

exp = Function(sym.exp)

log = Function(sym.log)

log10 = Log10(sym.log)

sin = Function(sym.sin)

cos = Function(sym.cos)

tan = Function(sym.tan)

cot = Function(sym.cot)

asin = Function(sym.asin)

acos = Function(sym.acos)

atan = Function(sym.atan)

atan2 = Function(sym.atan2)

acot = Function(sym.acot)

sinh = Function(sym.sinh)

cosh = Function(sym.cosh)

tanh = Function(sym.tanh)

asinh = Function(sym.asinh)

acosh = Function(sym.acosh)

atanh = Function(sym.atanh)

gcd = Function(sym.gcd)

u = H = heaviside = Heaviside = Function(sym.Heaviside)

delta = DiracDelta = Function(sym.DiracDelta)

from sympy.core import S, Integer
from sympy.core.logic import fuzzy_not


class UnitImpulse(sym.Function):

    is_integer = True
    
    @classmethod
    def eval(cls, nval):
        """
        Evaluates the discrete unit impulse function.
        """
        
        if nval.is_zero:
            return S.One
        elif fuzzy_not(nval.is_zero):
            return S.Zero


ui = unitimpulse = Function(UnitImpulse)


class UnitStep(sym.Function):

    is_integer = True
    
    @classmethod
    def eval(cls, nval):
        """
        Evaluates the discrete unit step function.
        """
        
        if nval.is_nonnegative:
            return S.One
        elif nval.is_negative:
            return S.Zero

us = unitstep = Function(UnitStep)


from .expr import Expr
