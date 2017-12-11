from crash import *

a = JavaCrash()
a.name_package="hahaha"
a.p_t_id=123
a.reason="reasonadadad"
a.stack_trace.append("nihao")
a.stack_trace.append("haodhaofaga")
a.occurred_time="12:13"

b=JavaCrash()
b.name_package=a.name_package
b.reason=a.reason

print a.is_same(b)

a.to_string()