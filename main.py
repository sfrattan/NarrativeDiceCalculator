from NarrativeDice import *
# from DiceDicts import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze some dice.')
    parser.add_argument('dice', type=str, nargs='+',
                        help='types: (B)oost, (S)etback, (A)bility, (D)ifficulty, (P)roficiency, (C)hallenge')
    parser.add_argument('-s', '--summary', action='store_true',
                        help='summary of outcome probabilities')
    parser.add_argument('-d', '--discrete', action='store_true',
                        help='discrete probabilities per symbol count')
    parser.add_argument('-c', '--cumulative', action='store_true',
                        help='probabilities of at least a given symbol count')

    # TODO: -e 'export' option with following argument for filename(s) and filetype (JSON or CSV)
    # TODO: -v 'verbose' option for use with export to also print results to terminal
    # TODO: check man pages for other programs to see their write-to-file arguments/usage

    args = parser.parse_args()

    # Generate a list of dice from args
    dice_list = []
    for d in args.dice:
        if d.lower() in ['b', 'boost']:
            dice_list.append(boost.copy())
        elif d.lower() in ['s', 'setback']:
            dice_list.append(setback.copy())
        elif d.lower() in ['a', 'ability']:
            dice_list.append(ability.copy())
        elif d.lower() in ['d', 'difficulty']:
            dice_list.append(difficulty.copy())
        elif d.lower() in ['p', 'proficiency']:
            dice_list.append(proficiency.copy())
        elif d.lower() in ['c', 'challenge']:
            dice_list.append(challenge.copy())
        else:
            # TODO: Syntax error on exit(2)
            exit(2)

    # dice_pool_data = DicePoolReporter(dice_list)


    # Create a root node for the tree of dice outcomes
    dice_tree = DieNode(None, (0, 0, 0, 0))
    # Populate the tree of dice outcomes
    dice_tree.append_dice(dice_list)
    data = dice_tree.export_results()

    # TODO: adjust argument parsing for write-to-file vs. print-to-screen
    if args.summary or (not args.discrete and not args.cumulative):
        data.summary()
    if args.discrete:
        data.discrete()
    if args.cumulative:
        data.cumulative()
    print('')
