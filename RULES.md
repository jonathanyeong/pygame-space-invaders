# Rules of Space Invaders

## Player

- Can move left and right to the edge of the screen.
- Can fire a missle.
- Has 3 lives.
- Will lose a life if hit by an alien missile.
- Will lose game if all lives are lost. Or once the aliens reach the player.
- Get a score based on number and type of aliens killed.

## Aliens
- 5 rows of aliens
- 4 types of aliens:
  - First two rows give 10 points.
  - Second two rows give 20 points.
  - Last row (furthest away from player) gives 40 points.
  - Mothership (red) flies across the top of the screen, gives ??? points.
- Mothership doesn't fire anything
- They fire missiles randomly only from the front row.
- They can move through the barricade.
- Once they reach the edge of one side they move down one row and move towards
the other side.

## Music
- Music gets faster as aliens get closer to the player.

## Barricades
- Get slowly eroded by missiles
- 4 barricades
- Once the barricade has a hole a missile can pass through it. 
- It takes 4 missile shots to fully erode a section of a barricade.
- There are 10 sections that make up a single barricade.

## Missiles

- A player has to wait until the other missile has disappeared before they can
fire another one.
- There are two different types of alien missiles. The more common one travels slower
than the other type.
