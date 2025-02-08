import collections
import math

farmland_matrix = [[0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.5, 0.39999999999999925, 0.39999999999999925, 0.5, 0.5, 0.5, 0.5, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925],
[0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.5, 0.5, 0.5, 0.5, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.5, 0.39999999999999925],
[0.3000000000000005, 0.3000000000000005, 0.5, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.5, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.5, 0.39999999999999925, 0.5, 0.5, 0.5, 0.39999999999999925, 0.5, 0.39999999999999925, 0.5, 0.5, 0.5, 0.39999999999999925],
[0.3000000000000005, 0.39999999999999925, 0.5, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.5, 0.39999999999999925, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.5, 0.5, 0.39999999999999925, 0.5, 0.5, 0.39999999999999925, 0.3000000000000005, 0.5, 0.5, 0.5],
[0.39999999999999925, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.505, 0.40599999999999925, 0.3070000000000005, 0.40599999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.5, 0.5, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925],
[0.3000000000000005, 0.3000000000000005, 0.5, 0.5, 0.5, 0.5, 0.3000000000000005, 0.3000000000000005, 0.5, 0.5, 0.505, 0.505, 0.39999999999999925, 0.5, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.5, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925],
[0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.5, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005, 0.3000000000000005, 0.5, 0.51, 0.505, 0.40599999999999925, 0.40599999999999925, 0.40599999999999925, 0.40599999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.5, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925],
[0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.40599999999999925, 0.40599999999999925, 0.3000000000000005, 0.39999999999999925, 0.4119999999999992, 0.4119999999999992, 0.51, 0.40599999999999925, 0.40599999999999925, 0.40599999999999925, 0.40599999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.5],
[0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.3070000000000005, 0.41199999999999926, 0.4239999999999992, 0.32100000000000045, 0.4239999999999992, 0.4239999999999992, 0.4239999999999992, 0.4119999999999992, 0.4119999999999992, 0.4119999999999992, 0.40599999999999925, 0.4119999999999992, 0.40599999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.5, 0.39999999999999925],
[0.39999999999999925, 0.5, 0.5, 0.39999999999999925, 0.4119999999999992, 0.42999999999999916, 0.43599999999999917, 0.3350000000000003, 0.42999999999999916, 0.44199999999999917, 0.43599999999999917, 0.4239999999999992, 0.4239999999999992, 0.4239999999999992, 0.4179999999999992, 0.4119999999999992, 0.4119999999999992, 0.505, 0.39999999999999925, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005, 0.5, 0.5],
[0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.40599999999999925, 0.52, 0.535, 0.45999999999999924, 0.3490000000000002, 0.3490000000000002, 0.4599999999999991, 0.4659999999999991, 0.45999999999999913, 0.44199999999999917, 0.4539999999999992, 0.44199999999999917, 0.4179999999999992, 0.4179999999999992, 0.40599999999999925, 0.39999999999999925, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.5, 0.3000000000000005],
[0.39999999999999925, 0.39999999999999925, 0.40599999999999925, 0.4179999999999992, 0.4299999999999992, 0.545, 0.565, 0.56, 0.4659999999999991, 0.4779999999999991, 0.47799999999999904, 0.4779999999999991, 0.45999999999999913, 0.45999999999999924, 0.4479999999999992, 0.4479999999999992, 0.3350000000000003, 0.39999999999999925, 0.3000000000000005, 0.3070000000000005, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.5, 0.39999999999999925],
[0.3000000000000005, 0.39999999999999925, 0.52, 0.3350000000000003, 0.45999999999999924, 0.48399999999999915, 0.58, 0.48999999999999916, 0.5019999999999991, 0.4959999999999991, 0.5079999999999991, 0.5139999999999991, 0.5019999999999992, 0.49599999999999916, 0.56, 0.3560000000000001, 0.34200000000000025, 0.3140000000000005, 0.3000000000000005, 0.4119999999999992, 0.3000000000000005, 0.3070000000000005, 0.3070000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.5, 0.3000000000000005],
[0.3000000000000005, 0.3070000000000005, 0.4299999999999992, 0.37000000000000016, 0.565, 0.6, 0.62, 0.5379999999999991, 0.5379999999999991, 0.5379999999999991, 0.5319999999999991, 0.625, 0.605, 0.6, 0.4959999999999992, 0.37000000000000005, 0.35600000000000015, 0.3420000000000003, 0.3350000000000003, 0.4119999999999992, 0.4119999999999992, 0.3140000000000005, 0.3140000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.3000000000000005],
[0.3070000000000005, 0.3140000000000005, 0.3630000000000001, 0.4899999999999992, 0.4899999999999992, 0.62, 0.5679999999999993, 0.665, 0.69, 0.685, 0.68, 0.645, 0.645, 0.5679999999999993, 0.43299999999999983, 0.39099999999999985, 0.3770000000000001, 0.34900000000000025, 0.4539999999999992, 0.4299999999999992, 0.4239999999999992, 0.4119999999999992, 0.3070000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.3000000000000005, 0.3000000000000005],
[0.3070000000000005, 0.3280000000000004, 0.3839999999999999, 0.4959999999999992, 0.43999999999999956, 0.5739999999999993, 0.6099999999999993, 0.6459999999999995, 0.6699999999999997, 0.6459999999999995, 0.6519999999999995, 0.6279999999999993, 0.5309999999999995, 0.6099999999999993, 0.4749999999999996, 0.412, 0.3770000000000001, 0.45999999999999924, 0.55, 0.4539999999999992, 0.4299999999999992, 0.3140000000000005, 0.3140000000000005, 0.3070000000000005, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925, 0.3000000000000005, 0.3000000000000005, 0.3000000000000005, 0.39999999999999925],
[0.3140000000000005, 0.3420000000000002, 0.39799999999999974, 0.42599999999999966, 0.4959999999999996, 0.6099999999999993, 0.5799999999999994, 0.7120000000000001, 0.6359999999999993, 0.6219999999999994, 0.6429999999999993, 0.6149999999999995, 0.6359999999999995, 0.5939999999999993, 0.5309999999999993, 0.4679999999999997, 0.4469999999999996, 0.41200000000000003, 0.4959999999999992, 0.45999999999999924, 0.4479999999999992, 0.43599999999999917, 0.3210000000000005, 0.3070000000000005, 0.3070000000000005, 0.40599999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005, 0.3000000000000005],
[0.32100000000000045, 0.35600000000000015, 0.4119999999999996, 0.4679999999999997, 0.5519999999999995, 0.5729999999999994, 0.6009999999999995, 0.6849999999999994, 0.7199999999999994, 0.7409999999999993, 0.7339999999999997, 0.7689999999999997, 0.7409999999999995, 0.6849999999999994, 0.6359999999999993, 0.5799999999999993, 0.5449999999999993, 0.5859999999999992, 0.5199999999999991, 0.4959999999999992, 0.46599999999999925, 0.4479999999999992, 0.3140000000000005, 0.32100000000000045, 0.40599999999999925, 0.40599999999999925, 0.40599999999999925, 0.39999999999999925, 0.39999999999999925, 0.5, 0.3000000000000005],
[0.3280000000000004, 0.39099999999999985, 0.43299999999999955, 0.5029999999999997, 0.6009999999999994, 0.6429999999999993, 0.6639999999999994, 0.7339999999999995, 0.8249999999999996, 0.8319999999999996, 0.8109999999999995, 0.8109999999999995, 0.7899999999999995, 0.7339999999999995, 0.6989999999999994, 0.6709999999999994, 0.6879999999999997, 0.6459999999999994, 0.5619999999999992, 0.5499999999999993, 0.5019999999999992, 0.46599999999999914, 0.4479999999999992, 0.44199999999999917, 0.3280000000000004, 0.3070000000000005, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.3000000000000005],
[0.3280000000000004, 0.4049999999999999, 0.4469999999999995, 0.5449999999999996, 0.6149999999999994, 0.6709999999999995, 0.7409999999999995, 0.8109999999999995, 0.8599999999999998, 0.8529999999999996, 0.8669999999999998, 0.8459999999999996, 0.8459999999999996, 0.7969999999999995, 0.7689999999999994, 0.7339999999999992, 0.6639999999999993, 0.5939999999999993, 0.6579999999999996, 0.6039999999999993, 0.4609999999999995, 0.4839999999999992, 0.47199999999999925, 0.33500000000000035, 0.3070000000000005, 0.39999999999999925, 0.3000000000000005, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925],
[0.3280000000000004, 0.4259999999999998, 0.4819999999999995, 0.5799999999999996, 0.6499999999999996, 0.7199999999999995, 0.8109999999999996, 0.8800000000000001, 0.9160000000000003, 0.9019999999999997, 0.9019999999999999, 0.8809999999999997, 0.8669999999999995, 0.8599999999999998, 0.8459999999999995, 0.8529999999999996, 0.7409999999999993, 0.6919999999999992, 0.6569999999999995, 0.6699999999999996, 0.6399999999999993, 0.5739999999999993, 0.4119999999999998, 0.3560000000000002, 0.3350000000000003, 0.40599999999999925, 0.40599999999999925, 0.40599999999999925, 0.39999999999999925, 0.39999999999999925, 0.39999999999999925],
[0.4539999999999992, 0.44699999999999973, 0.48899999999999955, 0.6079999999999995, 0.6709999999999995, 0.7409999999999995, 0.8800000000000001, 0.8920000000000001, 0.8879999999999997, 0.9019999999999997, 0.9019999999999999, 0.8949999999999997, 0.9019999999999997, 0.9089999999999998, 0.8879999999999997, 0.8669999999999998, 0.8109999999999995, 0.7409999999999993, 0.7059999999999994, 0.6819999999999997, 0.6519999999999996, 0.5099999999999993, 0.4259999999999996, 0.36300000000000004, 0.3280000000000004, 0.3350000000000003, 0.3070000000000005, 0.3140000000000005, 0.3070000000000005, 0.3000000000000005, 0.3000000000000005],
[0.363, 0.4539999999999998, 0.5239999999999996, 0.6219999999999996, 0.7129999999999995, 0.7969999999999996, 0.892, 0.9019999999999999, 0.9089999999999999, 0.9089999999999998, 0.9089999999999998, 0.9089999999999998, 0.9019999999999999, 0.9089999999999998, 0.9019999999999997, 0.8879999999999997, 0.8529999999999996, 0.7899999999999995, 0.7619999999999993, 0.7129999999999994, 0.5939999999999994, 0.5309999999999993, 0.4749999999999996, 0.4189999999999997, 0.3769999999999999, 0.35600000000000004, 0.32100000000000045, 0.32100000000000045, 0.3070000000000005, 0.3000000000000005, 0.3000000000000005],
[0.45999999999999924, 0.46799999999999964, 0.5379999999999995, 0.6429999999999996, 0.7549999999999994, 0.8389999999999996, 0.8809999999999998, 0.8879999999999998, 0.9089999999999998, 0.9159999999999998, 0.9299999999999998, 0.9299999999999998, 0.9089999999999998, 0.9299999999999998, 0.8949999999999997, 0.8809999999999997, 0.8739999999999997, 0.8319999999999994, 0.8109999999999994, 0.7759999999999995, 0.6779999999999994, 0.5939999999999993, 0.4959999999999992, 0.43999999999999967, 0.41899999999999954, 0.3979999999999997, 0.3420000000000002, 0.3280000000000004, 0.3140000000000005, 0.3000000000000005, 0.3000000000000005],
[0.3839999999999998, 0.4959999999999996, 0.5799999999999996, 0.6919999999999996, 0.7829999999999994, 0.8389999999999996, 0.9019999999999997, 0.9299999999999998, 0.9369999999999998, 0.9159999999999998, 0.9089999999999998, 0.9369999999999998, 0.9159999999999998, 0.9159999999999998, 0.9019999999999999, 0.8949999999999999, 0.8739999999999997, 0.8529999999999995, 0.8319999999999994, 0.7549999999999994, 0.6289999999999992, 0.5729999999999993, 0.5449999999999993, 0.4819999999999993, 0.5379999999999994, 0.4119999999999996, 0.34900000000000014, 0.3280000000000004, 0.3070000000000005, 0.41199999999999926, 0.3070000000000005],
[0.3839999999999998, 0.5239999999999996, 0.5939999999999996, 0.7269999999999996, 0.8389999999999996, 0.8669999999999998, 0.8949999999999999, 0.9159999999999999, 0.9159999999999999, 0.9299999999999998, 0.9369999999999998, 0.9299999999999998, 0.9089999999999999, 0.9229999999999998, 0.8949999999999997, 0.8739999999999998, 0.8599999999999998, 0.8319999999999996, 0.8109999999999995, 0.7199999999999994, 0.6429999999999992, 0.6289999999999992, 0.6079999999999992, 0.5169999999999992, 0.46799999999999925, 0.4119999999999996, 0.36300000000000004, 0.3490000000000002, 0.3280000000000004, 0.3140000000000005, 0.3070000000000005],
[0.4119999999999996, 0.5449999999999996, 0.6499999999999997, 0.7829999999999996, 0.8459999999999996, 0.8599999999999998, 0.9279999999999999, 0.9299999999999998, 0.946, 0.9299999999999998, 0.9159999999999999, 0.8949999999999997, 0.8160000000000004, 0.8080000000000004, 0.8320000000000003, 0.8320000000000003, 0.8669999999999995, 0.7760000000000005, 0.7520000000000004, 0.6720000000000006, 0.6849999999999994, 0.6569999999999994, 0.6149999999999991, 0.6459999999999995, 0.5979999999999993, 0.4679999999999994, 0.4049999999999997, 0.37699999999999995, 0.3490000000000002, 0.3280000000000004, 0.3070000000000005],
[0.43299999999999955, 0.5939999999999996, 0.6849999999999997, 0.7899999999999997, 0.8739999999999997, 0.9219999999999999, 0.9229999999999998, 0.9089999999999998, 0.9019999999999997, 0.9019999999999997, 0.8320000000000003, 0.8240000000000003, 0.7520000000000004, 0.7760000000000005, 0.8240000000000003, 0.8160000000000004, 0.8480000000000003, 0.7680000000000006, 0.8560000000000005, 0.7360000000000005, 0.7040000000000005, 0.6849999999999994, 0.706, 0.6639999999999996, 0.5979999999999993, 0.4679999999999992, 0.41899999999999954, 0.37699999999999995, 0.34900000000000025, 0.3420000000000003, 0.32100000000000045],
[0.4819999999999995, 0.6639999999999998, 0.7689999999999997, 0.8529999999999995, 0.8739999999999998, 0.9159999999999998, 0.9229999999999998, 0.8400000000000003, 0.8160000000000004, 0.8000000000000004, 0.7840000000000005, 0.7680000000000003, 0.7520000000000004, 0.9100000000000003, 0.935, 0.8400000000000003, 0.8240000000000003, 0.7840000000000004, 0.8319999999999994, 0.8500000000000003, 0.6960000000000006, 0.6400000000000006, 0.5520000000000007, 0.5729999999999993, 0.5169999999999992, 0.48199999999999926, 0.41899999999999943, 0.36999999999999994, 0.3490000000000002, 0.3350000000000004, 0.3140000000000005],
[0.5729999999999995, 0.7059999999999998, 0.7360000000000002, 0.8000000000000004, 0.7920000000000005, 0.8160000000000004, 0.8080000000000004, 0.7760000000000004, 0.7920000000000005, 0.7600000000000005, 0.8860000000000003, 0.9100000000000003, 0.9100000000000003, 0.9100000000000003, 0.8980000000000004, 0.8739999999999997, 0.8980000000000004, 0.7920000000000005, 0.8000000000000004, 0.6960000000000005, 0.8080000000000004, 0.7409999999999993, 0.5840000000000005, 0.6459999999999995, 0.5979999999999993, 0.5559999999999993, 0.4259999999999995, 0.3839999999999998, 0.34900000000000014, 0.3280000000000004, 0.3070000000000005],
[0.6289999999999997, 0.6960000000000002, 0.7840000000000004, 0.9159999999999999, 0.8240000000000003, 0.8160000000000005, 0.8080000000000005, 0.8000000000000004, 0.7840000000000005, 0.8860000000000003, 0.8860000000000003, 0.8529999999999996, 0.8740000000000003, 0.8740000000000003, 0.8740000000000003, 0.8319999999999996, 0.8620000000000004, 0.8560000000000003, 0.8500000000000004, 0.7040000000000006, 0.6560000000000007, 0.7360000000000002, 0.5440000000000006, 0.4080000000000004, 0.595, 0.47799999999999926, 0.3839999999999998, 0.3420000000000003, 0.32100000000000045, 0.3140000000000005, 0.3000000000000005],
[0.6720000000000003, 0.8720000000000002, 0.8720000000000003, 0.8080000000000004, 0.7920000000000005, 0.8680000000000004, 0.8680000000000004, 0.8620000000000004, 0.8620000000000004, 0.8319999999999994, 0.8249999999999996, 0.8039999999999995, 0.7759999999999995, 0.7759999999999995, 0.7960000000000005, 0.7900000000000006, 0.7129999999999994, 0.7540000000000003, 0.7480000000000002, 0.7180000000000003, 0.5600000000000007, 0.4960000000000006, 0.675, 0.35199999999999987, 0.3630000000000001, 0.3560000000000001, 0.3420000000000002, 0.3350000000000003, 0.32100000000000045, 0.3070000000000005, 0.3000000000000005],
[1.0, 0.8480000000000003, 0.7200000000000004, 0.82, 0.7780000000000004, 0.7780000000000004, 0.7720000000000004, 0.6989999999999995, 0.6639999999999994, 0.6569999999999994, 0.6359999999999993, 0.688, 0.6149999999999993, 0.5939999999999992, 0.5659999999999993, 0.5169999999999991, 0.4889999999999992, 0.5559999999999995, 0.5319999999999994, 0.5079999999999995, 0.4119999999999997, 0.31199999999999967, 0.27199999999999963, 0.23199999999999965, 0.20799999999999963, 0.20799999999999963, 0.3070000000000005, 0.3070000000000005, 0.3070000000000005, 0.3070000000000005, 0.3070000000000005]]
farm = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

wind_vector = (3,7)

def create_firebreak_land(mat, fire_break_position):
    for x,y in fire_break_position:
        mat[x][y] = 0

def find_matrix_bounds(mat):
    high_x, high_y = float('-inf')
    low_x, low_y = float('inf')

    rows, cols = len(mat), len(mat[0])

    for r in range(rows):
        high_x = max(r, high_x)
        low_x = min(r, low_x)
        for c in range(cols):
            high_y = max(c, high_y)
            low_y = min(c, low_y)
    
    return high_x, low_x, high_y, low_y

def find_cluster_bounds(cluster):
    high_x, high_y = float('-inf')
    low_x, low_y = float('inf')

    for c in cluster:
        high_x = max(c[0], high_x)
        low_x = min(c[0], low_x)
        high_y = max(c[1], high_y)
        low_y = min(c[1], low_y)
    
    return high_x, low_x, high_y, low_y

def create_bound(high_cluster_x, low_cluster_x, high_cluster_y, low_cluster_y):
    boundary = []

    for x in range(low_cluster_x, high_cluster_x + 1):
        boundary.append((x, low_cluster_y)) 
        boundary.append((x, high_cluster_y))

    # Left and Right boundaries
    for y in range(low_cluster_y, high_cluster_y + 1):
        boundary.append((low_cluster_x, y))
        boundary.append((high_cluster_x, y))

    return boundary
        
def generate_structures(farm_mat, landX, landY, burn_cluster, wall_threshold):
    heuristic_cluster = assign_heuristic(burn_cluster, *find_matrix_bounds(farm), landX, landY, 0.3, 10)

    wall_generation = []
    strip_generation = []

    for info, coords in heuristic_cluster.items():
        if len(coords) < wall_threshold:
            wall_generation.append(create_bound(*find_cluster_bounds(coords)))
            continue

    return heuristic_cluster

def assign_heuristic(burn_cluster, high_farm_x, low_farm_x, high_farm_y, low_farm_y, land_len_x, land_len_y, decay_constant, chop):
    heuristic_cluster = {}

    farm_center = (((high_farm_x + low_farm_x)/2), ((high_farm_y + low_farm_y)/2))

    for info, coords in burn_cluster.items():
        COM_x = info[0]
        COM_y = info[1] 
        MOI = info[2]

        if COM_x not in range(low_farm_x, high_farm_x) and COM_y not in range(low_farm_y, high_farm_y):
            distance_from_farm = ((farm_center[0] - COM_x)**2 + (farm_center[1] - COM_y)**2)**0.5
        else:
            #automatically set the hueristic to 1 (HIGH PRIORITY)
            new_info = (COM_x, COM_y, info[2], 1, 1, 1)
            heuristic_cluster[new_info] = coords
            continue

        distance_heuristic = math.exp(-decay_constant * distance_from_farm)
        spread_heuristic = MOI/chop
        size_heuristic = len(coords) / (land_len_x * land_len_y)

        new_info = (COM_x, COM_y, info[2], distance_heuristic, spread_heuristic, size_heuristic)
        
        heuristic_cluster[new_info] = coords 

    return heuristic_cluster
    
            
def find_burn_probability_clusters(mat, threshold, cluster_size):
    burn_clusters = {}

    visited_land = set()  

    rows, cols = len(mat), len(mat[0])

    def bfs_helper(r, c):
        q = collections.deque()
        visited_land.add((r,c))
        q.append((r,c))

        current_cluster = [(r,c)]
        sum_x, sum_y, count = r, c, 1

        while q:
            row, col = q.popleft()
            dirs = [[1,0], [-1,0], [0,1], [0,-1]]

            for dr, dc in dirs:
                new_row, new_col = row + dr, col + dc

                if 0 <= new_row < rows and 0 <= new_col < cols:

                    if mat[new_row][new_col] >= threshold and (new_row, new_col) not in visited_land:
                        visited_land.add((new_row, new_col))
                        q.append((new_row, new_col))
                        current_cluster.append((new_row, new_col))
                        sum_x += new_row
                        sum_y += new_col
                        count += 1
        
        if len(current_cluster) >= cluster_size:
            moment_of_inertia = 0
            COM_x, COM_y = sum_x / count, sum_y / count

            moment_of_inertia = sum(
                ( (c[0] - COM_x) ** 2 + (c[1] - COM_y) ** 2 ) for c in current_cluster
            )

            moment_of_inertia /= len(current_cluster)
            
            burn_clusters[(COM_x, COM_y, moment_of_inertia)] = current_cluster


    for r in range(rows):
        for c in range(cols):
            if mat[r][c] >= threshold and (r,c) not in visited_land:
                bfs_helper(r, c)
    
    return burn_clusters

if __name__ == "__main__":
    clusters = find_burn_probability_clusters(farmland_matrix, 0.5, 4)

    print(clusters)