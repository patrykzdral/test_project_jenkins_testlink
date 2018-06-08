import os
import re
import operator
from shutil import copyfile

dates = {}
for filename in os.listdir("test-reports/"):
    dates[filename] = re.sub("[^\d]", "", filename)

copyfile(os.path.join("test-reports",
                      max(dates.items(),
                          key=operator.itemgetter(1))[0]),
         os.path.join("test-reports", "recent_test_result.xml"))
