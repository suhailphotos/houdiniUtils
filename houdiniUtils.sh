houdiniUtils() {
    local houdini_version="20.0.653"  # Default Houdini version
    local optional_command="$1"

    cd ~/Documents/matrix/applications/houdiniUtils || return 1

    # Check if the environment is already activated
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        if [ -z "$optional_command" = "-e" ]; then
            # Run environment setup only
            if [[ -z "$PYTHONPATH" && -z "$DYLD_INSERT_LIBRARIES" ]]; then
                export PYTHONPATH="/Applications/Houdini/Houdini${houdini_version}/Frameworks/Houdini.framework/Versions/Current/Resources/houdini/python3.10libs"
                export DYLD_INSERT_LIBRARIES="/Applications/Houdini/Houdini${houdini_version}/Frameworks/Houdini.framework/Versions/Current/Houdini"

                cd "/Applications/Houdini/Houdini${houdini_version}/Frameworks/Houdini.framework/Versions/Current/Resources" || return 1
                source ./houdini_setup || return 1
                cd - || return 1
            fi
        elif [ "$optional_command" = "-hou" ]; then
            # Run environment setup and importhou.py script
            if [[ -z "$PYTHONPATH" && -z "$DYLD_INSERT_LIBRARIES" ]]; then
                export PYTHONPATH="/Applications/Houdini/Houdini${houdini_version}/Frameworks/Houdini.framework/Versions/Current/Resources/houdini/python3.10libs"
                export DYLD_INSERT_LIBRARIES="/Applications/Houdini/Houdini${houdini_version}/Frameworks/Houdini.framework/Versions/Current/Houdini"

                cd "/Applications/Houdini/Houdini${houdini_version}/Frameworks/Houdini.framework/Versions/Current/Resources" || return 1
                source ./houdini_setup || return 1
            fi
            python3 ./importhou/importhou.py || return 1
            cd - || return 1
        else
            echo "Invalid optional command"
            return 1
        fi
    else
        # Activate the environment if not already activated
        source "$(poetry env info --path)/bin/activate" || return 1
        
        # Check if optional command provided
        if [ -n "$optional_command" ]; then
            if [ "$optional_command" = "-e" ]; then
                # Set environment variables only
                export PYTHONPATH="/Applications/Houdini/Houdini${houdini_version}/Frameworks/Houdini.framework/Versions/Current/Resources/houdini/python3.10libs"
                export DYLD_INSERT_LIBRARIES="/Applications/Houdini/Houdini${houdini_version}/Frameworks/Houdini.framework/Versions/Current/Houdini"

                cd "/Applications/Houdini/Houdini${houdini_version}/Frameworks/Houdini.framework/Versions/Current/Resources" || return 1
                source ./houdini_setup || return 1

            elif [ "$optional_command" = "-hou" ]; then
                # Run environment setup and importhou.py script
                if [[ -z "$PYTHONPATH" && -z "$DYLD_INSERT_LIBRARIES" ]]; then
                    export PYTHONPATH="/Applications/Houdini/Houdini${houdini_version}/Frameworks/Houdini.framework/Versions/Current/Resources/houdini/python3.10libs"
                    export DYLD_INSERT_LIBRARIES="/Applications/Houdini/Houdini${houdini_version}/Frameworks/Houdini.framework/Versions/Current/Houdini"

                    cd "/Applications/Houdini/Houdini${houdini_version}/Frameworks/Houdini.framework/Versions/Current/Resources" || return 1
                    source ./houdini_setup || return 1
                fi
                python3 ./importhou/importhou.py || return 1
                cd - || return 1
            else
                echo "Invalid optional command"
                return 1
            fi
        fi
    fi
}


