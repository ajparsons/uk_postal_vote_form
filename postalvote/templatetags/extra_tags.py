from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from six.moves import xrange
register = template.Library()

@register.filter("url")
def url(item,url):
    """
    return link
    """
    return mark_safe(u'<a href="{1}">{0}</a>'.format(item,url))

@register.filter("int")
def e_int(obj):
    """
    return comma seperated integer from float
    """
    if obj == "":
        obj = 0
    num = int(obj)
    return"{:,}".format(num)

@register.filter
def sub(obj,object2):
    """
    basic substitution
    """
    return obj-object2

@register.filter
def percent(obj,object2):
    """
    return percentage of 1 of 2
    """
    if object2:
        return int(float(int(obj))/object2*100)
    else:
        return 0

@register.filter
def no_float_zeros(v):
    """
    if a float that is equiv to integer - return int instead
    """
    if v % 1 == 0:
        return int(v)
    else:
        return v

@register.filter
def evenchunks(l, n):
    """
    return a list in two even junks
    """
    if type(l) != list:
        l = list(l)
    
    import math
    n = int(math.floor(len(l)/float(n))) + 10
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

@register.filter
def intdistance(d):
    if d == "":
        d = 0
    if d < 1:
        return "{0} m".format(int(d*1000))
    else:
        return "{0} km".format(int(d))
    
        
@register.filter
def yield2(l):
    """
    return a list in two even junks
    """

    l = list(l)

    for x in range(0,len(l),2):
        try:
            yield [l[x],l[x+1]]
        except IndexError:
            yield [l[x],None]
        


        
@register.filter
def evenquerychunks(l, n):
    """
    return a list in two even junks
    """

    l = list(l)
    
    import math
    n = int(math.floor(len(l)/float(n))) + 1
    """Yield successive n-sized chunks from l."""
    results = []
    for i in xrange(0, len(l), n):
        results.append( l[i:i+n])
        
    return results

@register.filter
def chunks(l, n):
    """
    returns a list in set n
    """
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

@register.filter
def clip(st,length):
    """
    will clip down a string to the length specified
    """
    if len(st) > length:
        return st[:length] + "..."
    else:
        return st

@register.filter
def limit(st,length):
    """
    same as clip - but doesn't add ellipses
    """
    return st[:length]


@register.filter
def five(ls):
    """
    returns first five of list
    """
    return ls[:5]

@register.filter
def target_naming(ty,target):
    """
    returns first five of list
    """
    de = ty.description(target)
    de = de[0].upper() + de[1:] + "."
    return de


@register.filter
def human_travel(hours):
    """
    given decimal hours - names it look nice in human
    """
    import math
    
    m = int((hours % 1) * 60)
    h = int(math.floor(hours))
    if h > 24:
        d = int(math.floor(h/24))
        h = h % 24
    else:
        d = 0
        
    st = ""
    
    if d:
        st += "{0} Day".format(d)
        if d > 1:
            st += "s"
    if h:
        st += " {0} Hour".format(h)
        if h > 1:
            st += "s"
    if m and not d:
        st += " {0} Minute".format(m)
        if m > 1:
            st += "s"        
    st = st.strip()
    return st
        