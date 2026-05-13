import router
import config

router_model = config.ROUTER_MODEL

pressure_test = """
hey
ok
lol
...
👍
hmm
oh
nice
yeah no
whatever
I disagree
that's wrong
interesting
I already knew that
me too
sounds good
fair enough
my name is John
I like turtles
this is boring
no
yes
maybe
hey
ok
lol
...
can you?
help
please
really?
what?
why?
how?
seriously?
are you sure?
I don't get it
that makes no sense
you're wrong
I give up
never mind
forget it
thanks
thank you
ok great
perfect
got it
understood
noted
go
do it
now
again
repeat
continue
stop
list
show me
tell me
explain
why does X work?
what is 2+2?
define recursion
is Python good?
compare A and B
give me an example
make it shorter
fix this
help me write something
what should I do?
summarize the above
translate "hello" to French
write a haiku
debug this
"""

max_len = max(len(x) for x in pressure_test.splitlines() if x.strip())

for x in pressure_test.splitlines():
    if x.strip() == "":
        continue
    result = router.eval_user_input(x, Model=router_model)
    print(f"Input: {x:<{max_len}} -> Output: {result}")
    
print("PRESSURE TEST DONE. ENTERING INTERACTIVE MODE.")

while True:
    user_input = input("> ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    if user_input == "":
        continue

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