from expander import expand

def test_trivial():
    assert list(expand("")) == [""]
    assert list(expand("hello")) == ["hello"]

def test_stray_braces():
    assert list(expand(":-{")) == [":-{"]
    assert list(expand("oh }{ nice")) == ["oh }{ nice"]

def test_single():
    assert list(expand("a.{}")) == ["a."]
    assert list(expand("a.{doc}")) == ["a.doc"]
    assert list(expand("a.{doc,txt}")) == ["a.doc", "a.txt"]
    assert list(expand("a.{1,2,3}")) == ["a.1", "a.2", "a.3"]
    assert list(expand("{good,bad} mood")) == ["good mood", "bad mood"]
    assert list(expand("just {2,3} drinks")) == ["just 2 drinks", "just 3 drinks"]
    assert list(expand("soft drink{,s}")) == ["soft drink", "soft drinks"]

def test_multiple():
    assert list(expand("{a}{b}{c}{d}{e}{f}")) == ["abcdef"]
    assert list(expand("{a}.{doc,txt}")) == ["a.doc", "a.txt"]
    assert list(expand("{a,b}.{doc}")) == ["a.doc", "b.doc"]
    assert list(expand("{a,b}.{doc,txt}")) == ["a.doc", "a.txt", "b.doc", "b.txt"]
    assert list(expand("{0,1,2,3,4,5,6,7,8,9}"*5)) == [format(i, "05") for i in range(10**5)]
    assert list(expand("{a}"*100)) == ["a"*100]
