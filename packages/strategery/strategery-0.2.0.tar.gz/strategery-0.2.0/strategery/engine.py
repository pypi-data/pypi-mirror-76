import inspect
import time

from strategery.exceptions import TaskError, StrategyError
from strategery.logging import BypassLogger
from strategery.strategy import get_strategy

logger = BypassLogger()

def execute(*args, targets, preprocessed):
    if type(preprocessed) is list or type(preprocessed) is tuple:
        # Convert lists/tuples to type-indexed dictionary
        preprocessed = { type(p): p for p in preprocessed }

    queue = get_strategy(targets, preprocessed=preprocessed)

    print('Processing strategy:', file=logger)
    for stage in queue:
        print([t.__name__ for t in stage],
              file=logger)
    print("\n", file=logger)

    # Populate with preprocessed
    processed = preprocessed

    for stage in queue:
        for task in stage:
            if task not in processed:
                try:
                    ts = time.time()

                    __assert_task_type(task)

                    dependencies = __resolve_task_dependencies(task, processed)
                    processed[task] = task(*dependencies)

                    te = time.time()
                    print('[%2.2f sec] Processed: %r ' % (te - ts, task.__name__),
                          file=logger)
                except Exception as e:
                    raise TaskError('Stategery failed at task {t}, found at "{f}:{l}".\n\nInner error:\n{et}: {e}'.format(
                        t=task.__name__,
                        et=type(e).__name__,
                        e=e,
                        f=inspect.getmodule(task).__file__,
                        l=task.__code__.co_firstlineno
                    ))

    return tuple([processed[t] for t in targets])

def __assert_task_type(task):
    if not inspect.isfunction(task) and not inspect.isclass(task):
        raise Exception("Task cannot be processed, '{t}' is not a function or a class.".format(t=task.__name__))


def __resolve_task_dependencies(task, processed):
    if not hasattr(task, 'dependencies'):
        return tuple()

    while hasattr(task, 'original_function'):
        task = task.original_function

    signature: inspect.Signature = inspect.signature(task)

    if len(signature.parameters) != len(task.dependencies):
        raise StrategyError('Stategery task {t} expects parameters {p}, @fed_by decorator only accounts for {d}'.format(
            t=task.__name__,
            p=[k for k in signature.parameters.keys()],
            d=[d.__name__ if hasattr(d, "__name__") else type(d)
               for d in task.dependencies]
        ))

    values = []
    for parameter, dependency in zip(signature.parameters.values(), task.dependencies):
        if dependency in processed:
            values.append(processed[dependency])
        elif parameter.default != inspect._empty:
            values.append(parameter.default)
        else:
            raise StrategyError('Strategery task {t} could not resolve parameter {p}.'.format(
                t=task.__name__,
                p=parameter.name
            ))
    return values