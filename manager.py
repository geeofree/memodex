from memodex.webapp import app
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Flask Project cli tool by Geoffrey Galagaran.")

    # New app flag
    parser.add_argument(
        '-n', '--newapp',
        nargs=1,
        help='Creates a new flask blueprint app with the given name'
    )

    # New app prefixed URL option flag
    parser.add_argument(
        '-p', '-pre', '--prefixed',
        action='store_true',
        help='Set whether or not the blueprint route should be url prefixed'
    )

    # Run flag
    parser.add_argument(
        '-r', '--run',
        action='store_true',
        help='Runs the Flask application'
    )

    # Run Debugger option flag
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Set Flask debugger state when you run the app'
    )

    args = parser.parse_args()

    if args.debug and not args.run:
        print('Debug flag can only be used when the run flag is inputted')

    if args.run:
        app.run(debug=args.debug)

    if args.newapp:
        appname = ''.join(args.newapp)

        if appname.isalpha():
            create_blueprint(appname, args.prefixed)
        else:
            print('Application name must be only alphanumeric characters')
