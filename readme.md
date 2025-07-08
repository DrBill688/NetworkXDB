Example output:
```
====> Direct: Parent4 == p4
QUERY: select * from nxdb_corpus where parent_type = 'Parent4' and parent_value = 'p4'
REC: ('Parent4', 'p4', 'Child4.1', 'c41')
REC: ('Parent4', 'p4', 'Child4.2', 'c42')
REC: ('Parent4', 'p4', 'Child4.3', 'c43')
REC: ('Parent4', 'p4', 'Child3.3', 'c33')
{
    "Parent4": {
        "p4": {
            "Child4.1": "c41",
            "Child4.2": "c42",
            "Child4.3": "c43",
            "Child3.3": "c33"
        }
    }
}
====> Down1: Parent4 when Child4.3 == c43
QUERY: select a.*
 from nxdb_corpus a
 where a.parent_type = 'Parent4'
 and a.child_type = 'Child4.3' and a.child_value = 'c43'
REC: ('Parent4', 'p4', 'Child4.3', 'c43')
{
    "Parent4": {
        "p4": {
            "Child4.3": "c43"
        }
    }
}
====> Down2: Parent 4 when Child4.3.1 == c431
QUERY: select a.*,b.*
 from nxdb_corpus a,nxdb_corpus b
 where a.parent_type = 'Parent4'
 and a.child_type = b.parent_type and a.child_value = b.parent_value  and b.child_type = 'Child4.3.1' and b.child_value = 'c431'
REC: ('Parent4', 'p4', 'Child4.3', 'c43', 'Child4.3', 'c43', 'Child4.3.1', 'c431')
{
    "Parent4": {
        "p4": {
            "Child4.3": {
                "c43": {
                    "Child4.3.1": "c431"
                }
            }
        }
    }
}
====> Down2 UP1: Parent 4 when Parent3 == p3
QUERY: select a.*,b.*
 from nxdb_corpus a,nxdb_corpus b
 where a.parent_type = 'Parent4'
 and a.child_type = b.child_type and a.child_value = b.child_value  and b.parent_type = 'Parent3' and b.parent_value = 'p3'
REC: ('Parent4', 'p4', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child3.3', 'c33')
{
    "Parent4": {
        "p4": {
            "Child3.3": {
                "c33": {
                    "Parent3": "p3"
                }
            }
        }
    }
}
====> Ugly: Parent 4 when Parent2 == p2
QUERY: select a.*,b.*,c.*,d.*
 from nxdb_corpus a,nxdb_corpus b,nxdb_corpus c,nxdb_corpus d
 where a.parent_type = 'Parent4'
 and a.child_type = b.child_type and a.child_value = b.child_value  and b.parent_type = c.parent_type and b.parent_value = c.parent_value  and c.child_type = d.child_type and c.child_value = d.child_value  and d.parent_type = 'Parent2' and d.parent_value = 'p2'
REC: ('Parent4', 'p4', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child2.3', 'c23', 'Parent2', 'p2', 'Child2.3', 'c23')
{
    "Parent4": {
        "p4": {
            "Child3.3": {
                "c33": {
                    "Parent3": {
                        "p3": {
                            "Child2.3": {
                                "c23": {
                                    "Parent2": "p2"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
====> Ugly: Parent 4 when Parent1 == p1
QUERY: select a.*,b.*,c.*,d.*,e.*,f.*
 from nxdb_corpus a,nxdb_corpus b,nxdb_corpus c,nxdb_corpus d,nxdb_corpus e,nxdb_corpus f
 where a.parent_type = 'Parent4'
 and a.child_type = b.child_type and a.child_value = b.child_value  and b.parent_type = c.parent_type and b.parent_value = c.parent_value  and c.child_type = d.child_type and c.child_value = d.child_value  and d.parent_type = e.parent_type and d.parent_value = e.parent_value  and e.child_type = f.child_type and e.child_value = f.child_value  and f.parent_type = 'Parent1' and f.parent_value = 'p1'
REC: ('Parent4', 'p4', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child2.3', 'c23', 'Parent2', 'p2', 'Child2.3', 'c23', 'Parent2', 'p2', 'Child1.3', 'c13', 'Parent1', 'p1', 'Child1.3', 'c13')
{
    "Parent4": {
        "p4": {
            "Child3.3": {
                "c33": {
                    "Parent3": {
                        "p3": {
                            "Child2.3": {
                                "c23": {
                                    "Parent2": {
                                        "p2": {
                                            "Child1.3": {
                                                "c13": {
                                                    "Parent1": "p1"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
====> Direct: Parent1 == p1
QUERY: select * from nxdb_corpus where parent_type = 'Parent1' and parent_value = 'p1'
REC: ('Parent1', 'p1', 'Child1.1', 'c14')
REC: ('Parent1', 'p1', 'Child1.2', 'c12')
REC: ('Parent1', 'p1', 'Child1.3', 'c13')
{
    "Parent1": {
        "p1": {
            "Child1.1": "c14",
            "Child1.2": "c12",
            "Child1.3": "c13"
        }
    }
}
====> Ugly: Parent 4 when Child1.1 == c14
QUERY: select a.*,b.*,c.*,d.*,e.*,f.*,g.*
 from nxdb_corpus a,nxdb_corpus b,nxdb_corpus c,nxdb_corpus d,nxdb_corpus e,nxdb_corpus f,nxdb_corpus g
 where a.parent_type = 'Parent4'
 and a.child_type = b.child_type and a.child_value = b.child_value  and b.parent_type = c.parent_type and b.parent_value = c.parent_value  and c.child_type = d.child_type and c.child_value = d.child_value  and d.parent_type = e.parent_type and d.parent_value = e.parent_value  and e.child_type = f.child_type and e.child_value = f.child_value  and f.parent_type = g.parent_type and f.parent_value = g.parent_value  and g.child_type = 'Child1.1' and g.child_value = 'c14'
REC: ('Parent4', 'p4', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child3.3', 'c33', 'Parent3', 'p3', 'Child2.3', 'c23', 'Parent2', 'p2', 'Child2.3', 'c23', 'Parent2', 'p2', 'Child1.3', 'c13', 'Parent1', 'p1', 'Child1.3', 'c13', 'Parent1', 'p1', 'Child1.1', 'c14')
{
    "Parent4": {
        "p4": {
            "Child3.3": {
                "c33": {
                    "Parent3": {
                        "p3": {
                            "Child2.3": {
                                "c23": {
                                    "Parent2": {
                                        "p2": {
                                            "Child1.3": {
                                                "c13": {
                                                    "Parent1": {
                                                        "p1": {
                                                            "Child1.1": "c14"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
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