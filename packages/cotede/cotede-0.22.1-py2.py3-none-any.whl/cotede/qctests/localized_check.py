

from .qctests import QCCheckVar


cfg = {"procedure": "GlobalRange", "dimension": "PRES",
        "subset": [
            {"condition": "> 0 AND <= 25", "minval": -2, "maxval": 37},
            {"condition": "> 25 AND <= 50", "minval": -2, "maxval": 36},
            ]
        }


def find(profile, cfg, query):
    assert "OR" not in query, "I'm not ready for OR clause"
    rule = re.compile('\ *[<|>]=?\ *\d+')
    limits = query.split("AND")
    idx = True
    for l in limits:
        assert rule.match(l)
        idx &= eval("profile['{}'] {}".format(cfg["dimension"], l))
    return idx


class LocalizedCheck(QCCheckVar):
    def test(self):
        assert cfg["dimension"] in profile.keys()
        assert hasattr(qctests, cfg["procedure"])
        Procedure = eval("qctests.{}".format(str(cfg["procedure"]).strip()))
        base_cfg = {k: cfg[k] for k in cfg if k != 'subset'}
        layers = []
        for s in cfg["subset"]:
            scfg = dict(base_cfg)
            for k in [k for k in s if k != 'condition']:
                scfg[k] = s[k]
            local = Procedure(profile, 'TEMP', scfg)
        
        output = layers[0]
        l = layers[1]
        d = profile[cfg["dimension"]]



