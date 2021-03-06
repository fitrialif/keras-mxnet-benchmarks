import os
import sys
import copy
import importlib
import traceback
sys.path.append('keras_example')

back = os.environ['KERAS_BACKEND']
GPU_NUM = int(os.environ['GPU_NUM'])
metrics = ["training_time", "max_memory", "training_accuracy", "test_accuracy"]
example_list = list()
result = dict()


def run_benchmark():
    result[back] = dict()
    test_summary = open('test_summary_' + str(back) +
                        str(GPU_NUM) + '.txt', 'w')

    #If example_list is not empty, use it as example set
    #Otherwise run all examples under keras_example folder
    example_dir = 'keras_example/'
    example_set = os.listdir(example_dir) \
                  if len(example_list) == 0 else example_list
    for fname in example_set:
        if fname.startswith('__init__'):
            continue
        module = fname[:-3] if fname.endswith('.py') else fname
        try:
            example = importlib.import_module(module)
            result[back][module] = copy.deepcopy(example.ret_dict)
            del sys.modules[module]
            output = ''
            output += "{backend:<20}\n".format(backend=back)
            output += "{describe:<40}".format(describe='exampe/metric')
            for metric in metrics:
                output += "{metric:<25}".format(metric=metric)
            output += '\n'
            output += "{module:<40}".format(module=module)
            for metric in metrics:
                output += "{metric:<25}".format(metric=result[back][module][metric])
            output += '\n'
        except Exception as e:
            output = ''
            output += '%s on %s with %s GPU(s) returned error\n%s\n:' \
                      % (module, back, str(GPU_NUM), traceback.format_exc())
        finally:
            test_summary.write(output)
            print output
    test_summary.close()

if __name__ == '__main__':
    run_benchmark()
