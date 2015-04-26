import argparse
import getpass


class PromptAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # If no value then we need to prompt for it...
        if len(values) == 0:
            values.append(getpass.getpass())

        # Save the results in the namespace using the destination
        # variable given to the constructor.
        setattr(namespace, self.dest, values)
