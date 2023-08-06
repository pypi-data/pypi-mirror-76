# import re
# from resources import VO, COSP
# from src.texting import index_nontab, after_nontab
# from resources import RN, TB, LF, COLF
#
#
# def tag(label, item):
#     i = index_nontab(label)
#     key, text = str(label), str(item)
#     if not key.endswith(')'):
#         key = f'{key[0:i]}[{key[i:]}]'
#     if re.search(LF, text):
#         t = ' ' * i
#         if (text.endswith('}') or text.endswith(']')) and not text.endswith(']]'):
#             text = RN.join(after_nontab([t + x for x in text.split(RN)]))
#         else:
#             text = RN.join([''] + ([t + TB + x for x in text.split(RN)]) + [TB])
#     return f"{key} ({text})"
#
#
# def tags(*labels, **items):
#     length = len(labels)
#     if length == 0:
#         label = ''
#     elif length == 1:
#         label = f'[{labels[0]}]'
#     else:
#         label = labels[0]
#         for v in labels[1:]:
#             label = tag(label, v)
#     for key, item in items.items():
#         label = label + COLF + tag(key, item)
#     return label
#
#
# def link(label, item):
#     l, m = str(label), str(item)
#     if l:
#         return l + COSP + m if m else l
#     else:
#         return m if m else VO
