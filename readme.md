```

====> Direct: Parent4 == p4

QUERY: select \* from nxdb\_corpus where parent\_type = 'Parent4' and parent\_value = 'p4'

REC: ('Parent4', 'p4', 'Child4.1', 'c41')

REC: ('Parent4', 'p4', 'Child4.2', 'c42')

REC: ('Parent4', 'p4', 'Child4.3', 'c43')

REC: ('Parent4', 'p4', 'Child3.3', 'c33')

{

&nbsp;   "Parent4": {

&nbsp;       "p4": {

&nbsp;           "Child4.1": "c41",

&nbsp;           "Child4.2": "c42",

&nbsp;           "Child4.3": "c43",

&nbsp;           "Child3.3": "c33"

&nbsp;       }

&nbsp;   }

}

====> Down1: Parent4 when Child4.3 == c43

QUERY: select a.\*

&nbsp;from nxdb\_corpus a

&nbsp;where a.parent\_type = 'Parent4'

&nbsp;and a.child\_type = 'Child4.3' and a.child\_value = 'c43'

REC: ('Parent4', 'p4', 'Child4.3', 'c43')

{

&nbsp;   "Parent4": {

&nbsp;       "p4": {

&nbsp;           "Child4.3": "c43"

&nbsp;       }

&nbsp;   }

}

====> Down2: Parent 4 when Child4.3.1 == c431

QUERY: select a.\*,b.\*

&nbsp;from nxdb\_corpus a,nxdb\_corpus b

&nbsp;where a.parent\_type = 'Parent4'

&nbsp;and a.child\_type = b.parent\_type and a.child\_value = b.parent\_value  and b.child\_type = 'Child4.3.1' and b.child\_value = 'c431'

REC: ('Parent4', 'p4', 'Child4.3', 'c43', 'Child4.3', 'c43', 'Child4.3.1', 'c431')

{

&nbsp;   "Parent4": {

&nbsp;       "p4": {

&nbsp;           "Child4.3": {

&nbsp;               "c43": {

&nbsp;                   "Child4.3.1": "c431"

&nbsp;               }

&nbsp;           }

&nbsp;       }

&nbsp;   }

}

====> Down2 UP1: Parent 4 when Parent3 == p3

QUERY: select a.\*,b.\*

&nbsp;from nxdb\_corpus a,nxdb\_corpus b

&nbsp;where a.parent\_type = 'Parent4'

&nbsp;and a.child\_type = b.child\_type and a.child\_value = b.child\_value  and b.parent\_type = 'Parent3' and b.parent\_value = 'p3'

REC: ('Parent4', 'p4', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child3.3', 'c33')

{

&nbsp;   "Parent4": {

&nbsp;       "p4": {

&nbsp;           "Child3.3": {

&nbsp;               "c33": {

&nbsp;                   "Parent3": "p3"

&nbsp;               }

&nbsp;           }

&nbsp;       }

&nbsp;   }

}

====> Ugly: Parent 4 when Parent2 == p2

QUERY: select a.\*,b.\*,c.\*,d.\*

&nbsp;from nxdb\_corpus a,nxdb\_corpus b,nxdb\_corpus c,nxdb\_corpus d

&nbsp;where a.parent\_type = 'Parent4'

&nbsp;and a.child\_type = b.child\_type and a.child\_value = b.child\_value  and b.parent\_type = c.parent\_type and b.parent\_value = c.parent\_value  and c.child\_type = d.child\_type and c.child\_value = d.child\_value  and d.parent\_type = 'Parent2' and d.parent\_value = 'p2'

REC: ('Parent4', 'p4', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child2.3', 'c23', 'Parent2', 'p2', 'Child2.3', 'c23')

{

&nbsp;   "Parent4": {

&nbsp;       "p4": {

&nbsp;           "Child3.3": {

&nbsp;               "c33": {

&nbsp;                   "Parent3": {

&nbsp;                       "p3": {

&nbsp;                           "Child2.3": {

&nbsp;                               "c23": {

&nbsp;                                   "Parent2": "p2"

&nbsp;                               }

&nbsp;                           }

&nbsp;                       }

&nbsp;                   }

&nbsp;               }

&nbsp;           }

&nbsp;       }

&nbsp;   }

}

====> Ugly: Parent 4 when Parent1 == p1

QUERY: select a.\*,b.\*,c.\*,d.\*,e.\*,f.\*

&nbsp;from nxdb\_corpus a,nxdb\_corpus b,nxdb\_corpus c,nxdb\_corpus d,nxdb\_corpus e,nxdb\_corpus f

&nbsp;where a.parent\_type = 'Parent4'

&nbsp;and a.child\_type = b.child\_type and a.child\_value = b.child\_value  and b.parent\_type = c.parent\_type and b.parent\_value = c.parent\_value  and c.child\_type = d.child\_type and c.child\_value = d.child\_value  and d.parent\_type = e.parent\_type and d.parent\_value = e.parent\_value  and e.child\_type = f.child\_type and e.child\_value = f.child\_value  and f.parent\_type = 'Parent1' and f.parent\_value = 'p1'

REC: ('Parent4', 'p4', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child2.3', 'c23', 'Parent2', 'p2', 'Child2.3', 'c23', 'Parent2', 'p2', 'Child1.3', 'c13', 'Parent1', 'p1', 'Child1.3', 'c13')

{

&nbsp;   "Parent4": {

&nbsp;       "p4": {

&nbsp;           "Child3.3": {

&nbsp;               "c33": {

&nbsp;                   "Parent3": {

&nbsp;                       "p3": {

&nbsp;                           "Child2.3": {

&nbsp;                               "c23": {

&nbsp;                                   "Parent2": {

&nbsp;                                       "p2": {

&nbsp;                                           "Child1.3": {

&nbsp;                                               "c13": {

&nbsp;                                                   "Parent1": "p1"

&nbsp;                                               }

&nbsp;                                           }

&nbsp;                                       }

&nbsp;                                   }

&nbsp;                               }

&nbsp;                           }

&nbsp;                       }

&nbsp;                   }

&nbsp;               }

&nbsp;           }

&nbsp;       }

&nbsp;   }

}

====> Direct: Parent1 == p1

QUERY: select \* from nxdb\_corpus where parent\_type = 'Parent1' and parent\_value = 'p1'

REC: ('Parent1', 'p1', 'Child1.1', 'c14')

REC: ('Parent1', 'p1', 'Child1.2', 'c12')

REC: ('Parent1', 'p1', 'Child1.3', 'c13')

{

&nbsp;   "Parent1": {

&nbsp;       "p1": {

&nbsp;           "Child1.1": "c14",

&nbsp;           "Child1.2": "c12",

&nbsp;           "Child1.3": "c13"

&nbsp;       }

&nbsp;   }

}

====> Ugly: Parent 4 when Child1.1 == c14

QUERY: select a.\*,b.\*,c.\*,d.\*,e.\*,f.\*,g.\*

&nbsp;from nxdb\_corpus a,nxdb\_corpus b,nxdb\_corpus c,nxdb\_corpus d,nxdb\_corpus e,nxdb\_corpus f,nxdb\_corpus g

&nbsp;where a.parent\_type = 'Parent4'

&nbsp;and a.child\_type = b.child\_type and a.child\_value = b.child\_value  and b.parent\_type = c.parent\_type and b.parent\_value = c.parent\_value  and c.child\_type = d.child\_type and c.child\_value = d.child\_value  and d.parent\_type = e.parent\_type and d.parent\_value = e.parent\_value  and e.child\_type = f.child\_type and e.child\_value = f.child\_value  and f.parent\_type = g.parent\_type and f.parent\_value = g.parent\_value  and g.child\_type = 'Child1.1' and g.child\_value = 'c14'

REC: ('Parent4', 'p4', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child2.3', 'c23', 'Parent2', 'p2', 'Child2.3', 'c23', 'Parent2', 'p2', 'Child1.3', 'c13', 'Parent1', 'p1', 'Child1.3', 'c13', 'Parent1', 'p1', 'Child1.1', 'c14')

{

&nbsp;   "Parent4": {

&nbsp;       "p4": {

&nbsp;           "Child3.3": {

&nbsp;               "c33": {

&nbsp;                   "Parent3": {

&nbsp;                       "p3": {

&nbsp;                           "Child2.3": {

&nbsp;                               "c23": {

&nbsp;                                   "Parent2": {

&nbsp;                                       "p2": {

&nbsp;                                           "Child1.3": {

&nbsp;                                               "c13": {

&nbsp;                                                   "Parent1": {

&nbsp;                                                       "p1": {

&nbsp;                                                           "Child1.1": "c14"

&nbsp;                                                       }

&nbsp;                                                   }

&nbsp;                                               }

&nbsp;                                           }

&nbsp;                                       }

&nbsp;                                   }

&nbsp;                               }

&nbsp;                           }

&nbsp;                       }

&nbsp;                   }

&nbsp;               }

&nbsp;           }

&nbsp;       }

&nbsp;   }

}

Parent3

-- Child3.1 ( Ex. "c31")

-- Child3.2 ( Ex. "c32")

-- Child3.3 ( Ex. "c33", "c33")

-- Child2.3 ( Ex. "c23", "c23")

Parent4 (This is a description of what Parent4 nodes represent.)

-- Child4.1 ( Ex. "c41")

-- Child4.2 ( Ex. "c42")

-- Child4.3 ( Ex. "c43")

---- Child4.3.1 (This is a description of what Child4.3.1 nodes represent. Ex. "c431")

-- Child3.3 ( Ex. "c33", "c33")

Parent2

-- Child2.1 ( Ex. "c21")

-- Child2.2 ( Ex. "c22")

-- Child2.3 ( Ex. "c23", "c23")

-- Child1.3 ( Ex. "c13", "c13")

Parent1 (This is a description of what Parent1 nodes represent.)

-- Child1.1 ( Ex. "c14")

-- Child1.2 ( Ex. "c12")

-- Child1.3 ( Ex. "c13", "c13")

```

