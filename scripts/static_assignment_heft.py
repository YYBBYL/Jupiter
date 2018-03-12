dag = ['localpro',
 {'aggregate0': ['1',
                 'true',
                 'simpledetector0',
                 'astutedetector0',
                 'dftdetector0',
                 'teradetector0'],
  'aggregate1': ['1',
                 'true',
                 'simpledetector1',
                 'astutedetector1',
                 'dftdetector1',
                 'teradetector1'],
  'aggregate2': ['1',
                 'true',
                 'simpledetector2',
                 'astutedetector2',
                 'dftdetector2',
                 'teradetector2'],
  'astutedetector0': ['1', 'true', 'fusioncenter0'],
  'astutedetector1': ['1', 'true', 'fusioncenter1'],
  'astutedetector2': ['1', 'true', 'fusioncenter2'],
  'dftdetector0': ['1',
                   'true',
                   'fusioncenter0',
                   'dftslave00',
                   'dftslave01',
                   'dftslave02'],
  'dftdetector1': ['1',
                   'true',
                   'fusioncenter1',
                   'dftslave10',
                   'dftslave11',
                   'dftslave12'],
  'dftdetector2': ['1',
                   'true',
                   'fusioncenter2',
                   'dftslave20',
                   'dftslave21',
                   'dftslave22'],
  'dftslave00': ['1', 'false', 'dftslave00'],
  'dftslave01': ['1', 'false', 'dftslave01'],
  'dftslave02': ['1', 'false', 'dftslave02'],
  'dftslave10': ['1', 'false', 'dftslave10'],
  'dftslave11': ['1', 'false', 'dftslave11'],
  'dftslave12': ['1', 'false', 'dftslave12'],
  'dftslave20': ['1', 'false', 'dftslave20'],
  'dftslave21': ['1', 'false', 'dftslave21'],
  'dftslave22': ['1', 'false', 'dftslave22'],
  'fusioncenter0': ['4', 'true', 'globalfusion'],
  'fusioncenter1': ['4', 'true', 'globalfusion'],
  'fusioncenter2': ['4', 'true', 'globalfusion'],
  'globalfusion': ['3', 'true', 'home'],
  'localpro': ['1', 'false', 'aggregate0', 'aggregate1', 'aggregate2'],
  'simpledetector0': ['1', 'true', 'fusioncenter0'],
  'simpledetector1': ['1', 'true', 'fusioncenter1'],
  'simpledetector2': ['1', 'true', 'fusioncenter2'],
  'teradetector0': ['1', 'true', 'fusioncenter0', 'teramaster0'],
  'teradetector1': ['1', 'true', 'fusioncenter1', 'teramaster1'],
  'teradetector2': ['1', 'true', 'fusioncenter2', 'teramaster2'],
  'teramaster0': ['1', 'false', 'teraworker00', 'teraworker01', 'teraworker02'],
  'teramaster1': ['1', 'false', 'teraworker10', 'teraworker11', 'teraworker12'],
  'teramaster2': ['1', 'false', 'teraworker20', 'teraworker21', 'teraworker22'],
  'teraworker00': ['1', 'false', 'teraworker00'],
  'teraworker01': ['1', 'false', 'teraworker01'],
  'teraworker02': ['1', 'false', 'teraworker02'],
  'teraworker10': ['1', 'false', 'teraworker10'],
  'teraworker11': ['1', 'false', 'teraworker11'],
  'teraworker12': ['1', 'false', 'teraworker12'],
  'teraworker20': ['1', 'false', 'teraworker20'],
  'teraworker21': ['1', 'false', 'teraworker21'],
  'teraworker22': ['1', 'false', 'teraworker22']},
 {'aggregate0': 'node1',
  'aggregate1': 'node10',
  'aggregate2': 'node11',
  'astutedetector0': 'node11',
  'astutedetector1': 'node7',
  'astutedetector2': 'node6',
  'dftdetector0': 'node12',
  'dftdetector1': 'node9',
  'dftdetector2': 'node8',
  'dftslave00': 'node51',
  'dftslave01': 'node83',
  'dftslave02': 'node34',
  'dftslave10': 'node45',
  'dftslave11': 'node63',
  'dftslave12': 'node75',
  'dftslave20': 'node3',
  'dftslave21': 'node39',
  'dftslave22': 'node7',
  'fusioncenter0': 'node1',
  'fusioncenter1': 'node11',
  'fusioncenter2': 'node10',
  'globalfusion': 'node1',
  'localpro': 'node1',
  'simpledetector0': 'node10',
  'simpledetector1': 'node5',
  'simpledetector2': 'node4',
  'teradetector0': 'node1',
  'teradetector1': 'node2',
  'teradetector2': 'node3',
  'teramaster0': 'node31',
  'teramaster1': 'node56',
  'teramaster2': 'node83',
  'teraworker00': 'node65',
  'teraworker01': 'node6',
  'teraworker02': 'node18',
  'teraworker10': 'node26',
  'teraworker11': 'node51',
  'teraworker12': 'node52',
  'teraworker20': 'node32',
  'teraworker21': 'node6',
  'teraworker22': 'node72'}]
schedule = ['localpro',
 {'aggregate0': ['1',
                 'true',
                 'simpledetector0',
                 'astutedetector0',
                 'dftdetector0',
                 'teradetector0'],
  'aggregate1': ['1',
                 'true',
                 'simpledetector1',
                 'astutedetector1',
                 'dftdetector1',
                 'teradetector1'],
  'aggregate2': ['1',
                 'true',
                 'simpledetector2',
                 'astutedetector2',
                 'dftdetector2',
                 'teradetector2'],
  'astutedetector0': ['1', 'true', 'fusioncenter0'],
  'astutedetector1': ['1', 'true', 'fusioncenter1'],
  'astutedetector2': ['1', 'true', 'fusioncenter2'],
  'dftdetector0': ['1',
                   'true',
                   'fusioncenter0',
                   'dftslave00',
                   'dftslave01',
                   'dftslave02'],
  'dftdetector1': ['1',
                   'true',
                   'fusioncenter1',
                   'dftslave10',
                   'dftslave11',
                   'dftslave12'],
  'dftdetector2': ['1',
                   'true',
                   'fusioncenter2',
                   'dftslave20',
                   'dftslave21',
                   'dftslave22'],
  'dftslave00': ['1', 'false', 'dftslave00'],
  'dftslave01': ['1', 'false', 'dftslave01'],
  'dftslave02': ['1', 'false', 'dftslave02'],
  'dftslave10': ['1', 'false', 'dftslave10'],
  'dftslave11': ['1', 'false', 'dftslave11'],
  'dftslave12': ['1', 'false', 'dftslave12'],
  'dftslave20': ['1', 'false', 'dftslave20'],
  'dftslave21': ['1', 'false', 'dftslave21'],
  'dftslave22': ['1', 'false', 'dftslave22'],
  'fusioncenter0': ['4', 'true', 'globalfusion'],
  'fusioncenter1': ['4', 'true', 'globalfusion'],
  'fusioncenter2': ['4', 'true', 'globalfusion'],
  'globalfusion': ['3', 'true', 'home'],
  'localpro': ['1', 'false', 'aggregate0', 'aggregate1', 'aggregate2'],
  'simpledetector0': ['1', 'true', 'fusioncenter0'],
  'simpledetector1': ['1', 'true', 'fusioncenter1'],
  'simpledetector2': ['1', 'true', 'fusioncenter2'],
  'teradetector0': ['1', 'true', 'fusioncenter0', 'teramaster0'],
  'teradetector1': ['1', 'true', 'fusioncenter1', 'teramaster1'],
  'teradetector2': ['1', 'true', 'fusioncenter2', 'teramaster2'],
  'teramaster0': ['1', 'false', 'teraworker00', 'teraworker01', 'teraworker02'],
  'teramaster1': ['1', 'false', 'teraworker10', 'teraworker11', 'teraworker12'],
  'teramaster2': ['1', 'false', 'teraworker20', 'teraworker21', 'teraworker22'],
  'teraworker00': ['1', 'false', 'teraworker00'],
  'teraworker01': ['1', 'false', 'teraworker01'],
  'teraworker02': ['1', 'false', 'teraworker02'],
  'teraworker10': ['1', 'false', 'teraworker10'],
  'teraworker11': ['1', 'false', 'teraworker11'],
  'teraworker12': ['1', 'false', 'teraworker12'],
  'teraworker20': ['1', 'false', 'teraworker20'],
  'teraworker21': ['1', 'false', 'teraworker21'],
  'teraworker22': ['1', 'false', 'teraworker22']},
 {'aggregate0': ['aggregate0', 'ubuntu-2gb-sfo1-05', 'root', 'PASSWORD'],
  'aggregate1': ['aggregate1', 'ubuntu-2gb-sfo1-01', 'root', 'PASSWORD'],
  'aggregate2': ['aggregate2', 'ubuntu-2gb-sfo1-02', 'root', 'PASSWORD'],
  'astutedetector0': ['astutedetector0',
                      'ubuntu-2gb-sfo1-02',
                      'root',
                      'PASSWORD'],
  'astutedetector1': ['astutedetector1',
                      'ubuntu-2gb-nyc2-02',
                      'root',
                      'PASSWORD'],
  'astutedetector2': ['astutedetector2',
                      'ubuntu-2gb-fra1-02',
                      'root',
                      'PASSWORD'],
  'dftdetector0': ['dftdetector0',
                   'ubuntu-s-1vcpu-3gb-sgp1-01',
                   'root',
                   'PASSWORD'],
  'dftdetector1': ['dftdetector1', 'ubuntu-2gb-nyc2-04', 'root', 'PASSWORD'],
  'dftdetector2': ['dftdetector2', 'ubuntu-2gb-nyc2-03', 'root', 'PASSWORD'],
  'dftslave00': ['dftslave00',
                 'ubuntu-s-1vcpu-3gb-nyc3-01',
                 'root',
                 'PASSWORD'],
  'dftslave01': ['dftslave01',
                 'ubuntu-s-1vcpu-3gb-fra1-05',
                 'root',
                 'PASSWORD'],
  'dftslave02': ['dftslave02',
                 'ubuntu-s-1vcpu-3gb-ams3-06',
                 'root',
                 'PASSWORD'],
  'dftslave10': ['dftslave10',
                 'ubuntu-s-1vcpu-3gb-lon1-09',
                 'root',
                 'PASSWORD'],
  'dftslave11': ['dftslave11',
                 'ubuntu-s-1vcpu-3gb-sfo2-02',
                 'root',
                 'PASSWORD'],
  'dftslave12': ['dftslave12',
                 'ubuntu-s-1vcpu-3gb-tor1-05',
                 'root',
                 'PASSWORD'],
  'dftslave20': ['dftslave20', 'ubuntu-2gb-sfo1-03', 'root', 'PASSWORD'],
  'dftslave21': ['dftslave21',
                 'ubuntu-s-1vcpu-3gb-lon1-03',
                 'root',
                 'PASSWORD'],
  'dftslave22': ['dftslave22', 'ubuntu-2gb-nyc2-02', 'root', 'PASSWORD'],
  'fusioncenter0': ['fusioncenter0', 'ubuntu-2gb-sfo1-05', 'root', 'PASSWORD'],
  'fusioncenter1': ['fusioncenter1', 'ubuntu-2gb-sfo1-02', 'root', 'PASSWORD'],
  'fusioncenter2': ['fusioncenter2', 'ubuntu-2gb-sfo1-01', 'root', 'PASSWORD'],
  'globalfusion': ['globalfusion', 'ubuntu-2gb-sfo1-05', 'root', 'PASSWORD'],
  'home': ['home', 'ubuntu-2gb-ams2-04', 'root', 'PASSWORD'],
  'localpro': ['localpro', 'ubuntu-2gb-sfo1-05', 'root', 'PASSWORD'],
  'simpledetector0': ['simpledetector0',
                      'ubuntu-2gb-sfo1-01',
                      'root',
                      'PASSWORD'],
  'simpledetector1': ['simpledetector1',
                      'ubuntu-2gb-fra1-01',
                      'root',
                      'PASSWORD'],
  'simpledetector2': ['simpledetector2',
                      'ubuntu-2gb-ams2-03',
                      'root',
                      'PASSWORD'],
  'teradetector0': ['teradetector0', 'ubuntu-2gb-sfo1-05', 'root', 'PASSWORD'],
  'teradetector1': ['teradetector1',
                    'ubuntu-s-1vcpu-3gb-lon1-01',
                    'root',
                    'PASSWORD'],
  'teradetector2': ['teradetector2', 'ubuntu-2gb-sfo1-03', 'root', 'PASSWORD'],
  'teramaster0': ['teramaster0',
                  'ubuntu-s-1vcpu-3gb-ams3-03',
                  'root',
                  'PASSWORD'],
  'teramaster1': ['teramaster1',
                  'ubuntu-s-1vcpu-3gb-nyc3-06',
                  'root',
                  'PASSWORD'],
  'teramaster2': ['teramaster2',
                  'ubuntu-s-1vcpu-3gb-fra1-05',
                  'root',
                  'PASSWORD'],
  'teraworker00': ['teraworker00',
                   'ubuntu-s-1vcpu-3gb-sfo2-04',
                   'root',
                   'PASSWORD'],
  'teraworker01': ['teraworker01', 'ubuntu-2gb-fra1-02', 'root', 'PASSWORD'],
  'teraworker02': ['teraworker02',
                   'ubuntu-s-1vcpu-3gb-blr1-10',
                   'root',
                   'PASSWORD'],
  'teraworker10': ['teraworker10',
                   'ubuntu-s-1vcpu-3gb-nyc1-07',
                   'root',
                   'PASSWORD'],
  'teraworker11': ['teraworker11',
                   'ubuntu-s-1vcpu-3gb-nyc3-01',
                   'root',
                   'PASSWORD'],
  'teraworker12': ['teraworker12',
                   'ubuntu-s-1vcpu-3gb-nyc3-02',
                   'root',
                   'PASSWORD'],
  'teraworker20': ['teraworker20',
                   'ubuntu-s-1vcpu-3gb-ams3-04',
                   'root',
                   'PASSWORD'],
  'teraworker21': ['teraworker21', 'ubuntu-2gb-fra1-02', 'root', 'PASSWORD'],
  'teraworker22': ['teraworker22',
                   'ubuntu-s-1vcpu-3gb-tor1-08',
                   'root',
                   'PASSWORD']}]


profiler_ips={'home': '10.106.137.131',
 'node10': '10.98.63.209',
 'node11': '10.106.244.229',
 'node2': '10.98.85.113',
 'node3': '10.110.184.42',
 'node4': '10.104.15.239',
 'node5': '10.99.33.214',
 'node6': '10.109.139.20',
 'node7': '10.109.220.122',
 'node8': '10.101.74.227',
 'node9': '10.108.12.33'}

execution_ips = {'aggregate0': '10.96.57.107',
 'aggregate1': '10.96.57.107',
 'aggregate2': '10.96.57.107',
 'astutedetector0': '10.96.57.107',
 'astutedetector1': '10.96.57.107',
 'astutedetector2': '10.96.57.107',
 'dftdetector0': '10.96.57.107',
 'dftdetector1': '10.96.57.107',
 'dftdetector2': '10.96.57.107',
 'dftslave00': '10.111.52.111',
 'dftslave01': '10.106.161.77',
 'dftslave02': '10.102.203.115',
 'dftslave10': '10.109.33.141',
 'dftslave11': '10.106.108.240',
 'dftslave12': '10.110.242.192',
 'dftslave20': '10.102.20.128',
 'dftslave21': '10.104.99.224',
 'dftslave22': '10.99.64.47',
 'fusioncenter0': '10.96.57.107',
 'fusioncenter1': '10.96.57.107',
 'fusioncenter2': '10.96.57.107',
 'globalfusion': '10.96.57.107',
 'home': '10.96.57.107',
 'localpro': '10.96.57.107',
 'simpledetector0': '10.96.57.107',
 'simpledetector1': '10.96.57.107',
 'simpledetector2': '10.96.57.107',
 'teradetector0': '10.96.57.107',
 'teradetector1': '10.96.57.107',
 'teradetector2': '10.96.57.107',
 'teramaster0': '10.100.249.213',
 'teramaster1': '10.98.63.0',
 'teramaster2': '10.101.250.56',
 'teraworker00': '10.96.213.166',
 'teraworker01': '10.99.72.220',
 'teraworker02': '10.96.177.38',
 'teraworker10': '10.103.233.123',
 'teraworker11': '10.111.155.53',
 'teraworker12': '10.104.83.40',
 'teraworker20': '10.100.234.0',
 'teraworker21': '10.102.178.73',
 'teraworker22': '10.103.221.195'}
