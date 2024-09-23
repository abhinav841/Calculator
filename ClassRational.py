
#@ Sept 2021, Abhinav Anand


class Rational:

    '''A basic implementation of rational numbers

       Rational() -> 0 / 1
       Rational(int or str:a) -> rational a / 1
       Rational(int:a, int:b) -> rational a / b
       Rational(float or str:a) -> rational equivalent of a

       Note: power operation is implemented only for integer
       '''

    __slots__ = ("_num", "_den")

    def __init__(self, num = 0, den = None):
        if den == 0:
            raise ZeroDivisionError("denominator cannot be zero")
        if den != None and (isinstance(num, (str, float, Rational)) or not isinstance(den, int)) or not isinstance(num, (int, float, str, Rational)):
            raise ValueError("only int arguments or a float or a string argument")
        if den == None: den = 1
        if num:
            if isinstance(num, Rational):
                num, den = num._num, num._den
            elif isinstance(num, (float, str)):
                if float(num) in (float('inf'), float('-inf'), float('nan')):
                    raise ValueError("can't set non-real values")
                num, den = self._fromfloat(num)
            sign_num = 1 if num>=0 else -1
            sign_den = 1 if den>0 else -1
            self._num, self._den = self._reducefrac(abs(num), abs(den))
            self._num *= sign_num*sign_den
        else:
            self._num, self._den = 0, 1

    def _reducefrac(self, num, den):
        "Reduces a fraction to simplest form"
        swap = False
        if num < den:
            num, den = den, num
            swap = True
        a, b = num, den
        while (i := a % b):
            a, b = b, i
        if swap:
            return den//b, num//b
        else:
            return num//b, den//b

    def _fromfloat(self, num):
        "Converts float into fraction"
        strn = str(num)
        stmt = "'.' in b and b[::-1].find('.')"
        if 'e+' in strn:
            b, _, e = strn.partition('e+')
            return int(b.replace('.',''))*10**(int(e)-eval(stmt)), 1
        elif 'e-' in strn:
            b, _, e = strn.partition('e-')
            return int(b.replace('.','')), 10**(int(e)+eval(stmt))
        else:
            return int(strn.replace('.','')), 10**strn[::-1].find('.')

    def _typecheck(self, arg, opr):
        "Checks type validity"
        if isinstance(arg, Rational):
            return arg
        if isinstance(arg, (int, float)):
            return Rational(arg)
        raise TypeError(f"unsupported operand type(s) for {opr}: 'Rational' and '{type(arg).__name__}'")

    def __pos__(self):
        "+ self"
        return self

    def __neg__(self):
        "- self"
        return Rational(-self._num, self._den)

    def __abs__(self):
        "abs(self)"
        return Rational(abs(self._num), self._den)

    def __bool__(self):
        "numerator != 0"
        return bool(self._num)

    def __add__(self, other):
        "self + other"
        other = self._typecheck(other, '+')
        n1, d1 = self._num, self._den
        n2, d2 = other._num, other._den
        return Rational(n1*d2 + n2*d1, d1*d2)

    def __radd__(self, other):
        "other + self"
        return self.__add__(Rational(other))

    def __sub__(self, other):
        "self - other"
        other = self._typecheck(other, '-')
        n1, d1 = self._num, self._den
        n2, d2 = other._num, other._den
        return Rational(n1*d2 - n2*d1, d1*d2)

    def __rsub__(self, other):
        "other - self"
        return Rational(other).__sub__(self)

    def __mul__(self, other):
        "self * other"
        other = self._typecheck(other, '*')
        return Rational(self._num * other._num, self._den * other._den)

    def __rmul__(self, other):
        "other * self"
        return self.__mul__(Rational(other))

    def __truediv__(self, other):
        "self / other"
        other = self._typecheck(other, '/')
        return Rational(self._num * other._den, self._den * other._num)

    def __rtruediv__(self, other):
        "other / self"
        return Rational(other).__truediv__(self)

    def __pow__(self, value):
        "pow(self, value)"
        if isinstance(value, int):
            if value < 0:
                return Rational(self._den**abs(value), self._num**abs(value))
            return Rational(self._num**value, self._den**value)
        raise TypeError(f"unsupported operand type(s) for ** or pow(): 'Rational' and '{type(value).__name__}'")

    def __rpow__(self, value):
        "pow(value, self)"
        return value**self.value

    def __eq__(self, other):
        "self == other"
        if isinstance(other, (int, float)):
            return self == Rational(other)
        elif isinstance(other, Rational):
            return self._num == other._num and self._den == other._den
        return False

    def __lt__(self, other):
        "self < other"
        if isinstance(other, (int, float, Rational)):
            return self.__sub__(other)._num < 0
        raise TypeError(f"'<' not supported between instances of '{type(arg).__name__}' and 'Rational'")

    def __gt__(self, other):
        "self > other"
        if isinstance(other, (int, float, Rational)):
            return self.__sub__(other)._num > 0
        raise TypeError(f"'>' not supported between instances of '{type(arg).__name__}' and 'Rational'")

    def __le__(self, other):
        "self <= other"
        if isinstance(other, (int, float, Rational)):
            return self.__sub__(other)._num <= 0
        raise TypeError(f"'<=' not supported between instances of '{type(arg).__name__}' and 'Rational'")

    def __ge__(self, other):
        "self >= other"
        if isinstance(other, (int, float, Rational)):
            return self.__sub__(other)._num >= 0
        raise TypeError(f"'>=' not supported between instances of '{type(arg).__name__}' and 'Rational'")

    @property
    def numerator(self):
        return self._num

    @property
    def denominator(self):
        return self._den

    @property
    def value(self):
        if self._den == 1:
            return self._num
        return self._num / self._den

    def __repr__(self):
        return f"{self._num} / {self._den}"
        
