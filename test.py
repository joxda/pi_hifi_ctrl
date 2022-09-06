import libamp
import matplotlib.pyplot as plt
rc5c = libamp.build_rc5('CXA80','Power_On')

libamp.print_mnch(rc5c)

rc5c = libamp.build_rc5('CXA80','Power_Off')
libamp.print_mnch(rc5c)