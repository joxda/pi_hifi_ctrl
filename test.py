import libamp

rc5c = libamp.build_rc5('CXA80','Power_On')

libamp.print_mnch(rc5c)
libamp.execute(17, 'CXA80', 'Power_On', 3)
rc5c = libamp.build_rc5('CXA80','Power_Off')
libamp.print_mnch(rc5c)
