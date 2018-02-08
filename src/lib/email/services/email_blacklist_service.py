from ..models import EmailBlacklist


disallowed_domains = [
    '@a.com', '@b.com', '@c.com', '@d.com', '@e.com', '@f.com', '@g.com', '@h.com', '@i.com', '@j.com', '@k.com',
    '@l.com', '@m.com', '@n.com', '@o.com', '@p.com', '@q.com', '@r.com', '@s.com', '@t.com', '@u.com', '@v.com',
    '@w.com', '@x.com', '@y.com', '@z.com',
    '@a.net', '@b.net', '@c.net', '@d.net', '@e.net', '@f.net', '@g.net', '@h.net', '@i.net', '@j.net', '@k.net',
    '@l.net', '@m.net', '@n.net', '@o.net', '@p.net', '@q.net', '@r.net', '@s.net', '@t.net', '@u.net', '@v.net',
    '@w.net', '@x.net', '@y.net', '@z.net',
    '@a.kr', '@b.kr', '@c.kr', '@d.kr', '@e.kr', '@f.kr', '@g.kr', '@h.kr', '@i.kr', '@j.kr', '@k.kr',
    '@l.kr', '@m.kr', '@n.kr', '@o.kr', '@p.kr', '@q.kr', '@r.kr', '@s.kr', '@t.kr', '@u.kr', '@v.kr',
    '@w.kr', '@x.kr', '@y.kr', '@z.kr',
    '@aa.com', '@aaa.com', '@asf.com', '@ab.com', '@bc.com', '@asdf.com', '@cd.com', '@df.com', '@fg.com', '@hi.com'
    '@never.com', '@nnaver.com', '@gamil.com',
]


def add_blacklist(email: str) -> None:
    EmailBlacklist.objects.create(email=email)


def is_in_blacklist(email: str) -> bool:
    for disallowed_domain in disallowed_domains:
        if disallowed_domain in email:
            return True

    return EmailBlacklist.objects.is_in_blacklist(email)
