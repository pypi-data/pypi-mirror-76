# Tamagotchi-challenge
A PyGame implementation of the Tamagotchi challenge

## Installation instructions

Make sure to have python3 installed with the pip package installer.

You may also like to create a virtual environment to run it but it is not necessary.

`pip3 install -r requirements.txt`

## Running tests

From the base of the Tamagotchi Challenge directory, you can run

`python3 setup.py test`

This will run all the available unit tests and will make sure the correct packages are accessible.

## Running the game

Run in console

`python3 setup.py install`
`python3 -m tamagotchi`

## Controls

The user driven interactions with the pet is done through the keyboard.

There is a list of available foods on the bottom right hand corner that 
you may cycle through by pressing either the `left arrow key` or 
`right arrow key`.

The food showing in the box can be feed to the pet by pressing `e`.
Over-eating can fill the pets stomach and it will alleviate itself.

There are two gauges to view, the health and energy bar, the energy
bar will go redder and the pet will go to sleep. You may pre-empt an
automatic sleep by telling the pet to go to sleep by pressing `s`. The
health bar is recovered by eating food, and each type of food impacts
the pets health and fullness differently. Beware no health will cause
the pet to pass away.

The pet will age as time progresses, growing older which can be seen
by the change in art. Unfortunately as time goes on, the pet will
pass away and that will finish the game with the player having
successfully raised a pet having not neglected it.

## Aim of the game

You should try your best to take care of the pet by feeding it when
it gets hungry and drops health. Beware if it gets tired and goes to
sleep you may find yourself unable to feed your pet. Managing these
along with a limited food set, and other possible hindrances to feeding
your pet are the key to giving your pet the best longevity.

## Future development

The game board could be constructed by a factory, that will handle
producing the food inventory, the actor - pet etc.

Unifying food inventory and status bars under UI elements for the
purpose of drawing.

Need to fix up naming with the StatusBarFactory with StatusElement.

An actor factory that can create NPC actors, and extending the Actor
abstract class to include an interaction function that can take in
other actors in the game. From there we can extend to look at state
retained interactions from simple, 'Nice to see you again' to a
friendship tracker.

Extending OO design, random chance special food items like a golden apple 
could be implemented via decorators. The pet could be a singleton to 
ensure only one pet actually exists.

## Credit

I did not create any of the pixel art used and was taken from the web. Credit
to those who spent their time creating these pieces of art. These works are
not being used for the purpose of commercial use.