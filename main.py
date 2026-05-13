import router
import config

router_model = config.ROUTER_MODEL

while True:
    user_input = input("> ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    if user_input.startswith("/changemodel"):
        parts = user_input.split()
        if len(parts) == 2:
            new_model = parts[1]
            print(f"Changing router model to '{new_model}'")
            router_model = new_model
        else:
            print("Usage: /changemodel <model_name>")
        continue

    result = router.eval_user_input(user_input, Model=router_model)
    print(result)