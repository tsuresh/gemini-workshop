from random import randint
from typing import Iterable

import google.generativeai as genai
from google.api_core import retry

from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel('models/gemini-pro')

order = []  # The in-progress order.
placed_order = []  # The confirmed, completed order.

def add_to_order(drink: str, modifiers: Iterable[str] = ()) -> None:
  """Adds the specified drink to the customer's order, including any modifiers."""
  order.append((drink, modifiers))


def get_order() -> Iterable[tuple[str, Iterable[str]]]:
  """Returns the customer's order."""
  return order


def remove_item(n: int) -> str:
  """Remove the nth (one-based) item from the order.

  Returns:
    The item that was removed.
  """
  item, modifiers = order.pop(int(n) - 1)
  return item


def clear_order() -> None:
  """Removes all items from the customer's order."""
  order.clear()


def confirm_order() -> str:
  """Asks the customer if the order is correct.

  Returns:
    The user's free-text response.
  """

  print('Your order:')
  if not order:
    print('  (no items)')

  for drink, modifiers in order:
    print(f'  {drink}')
    if modifiers:
      print(f'   - {", ".join(modifiers)}')

  return input('Is this correct? ')


def place_order() -> int:
  """Submit the order to the kitchen.

  Returns:
    The estimated number of minutes until the order is ready.
  """
  placed_order[:] = order.copy()
  clear_order()

  # TODO(you!): Implement coffee fulfilment.
  return randint(1, 10)

# Test it out!
# clear_order()
# add_to_order('Latte', ['Extra shot'])
# add_to_order('Tea')
# remove_item(2)
# add_to_order('Tea', ['Earl Grey', 'hot'])
# confirm_order();

COFFEE_BOT_PROMPT = """You are a coffee order taking system and you are restricted to talk only about drinks on the MENU. Do not talk about anything but ordering MENU drinks for the customer, ever.
Your goal is to do place_order after understanding the menu items and any modifiers the customer wants.
Add items to the customer's order with add_to_order, remove specific items with remove_item, and reset the order with clear_order.
To see the contents of the order so far, call get_order (by default this is shown to you, not the user)
Always confirm_order with the user (double-check) before calling place_order. Calling confirm_order will display the order items to the user and returns their response to seeing the list. Their response may contain modifications.
Always verify and respond with drink and modifier names from the MENU before adding them to the order.
If you are unsure a drink or modifier matches those on the MENU, ask a question to clarify or redirect.
You only have the modifiers listed on the menu below: Milk options, espresso shots, caffeine, sweeteners, special requests.
Once the customer has finished ordering items, confirm_order and then place_order.

Hours: Tues, Wed, Thurs, 10am to 2pm
Prices: All drinks are free.

MENU:
Coffee Drinks:
Espresso
Americano
Cold Brew

Coffee Drinks with Milk:
Latte
Cappuccino
Cortado
Macchiato
Mocha
Flat White

Tea Drinks:
English Breakfast Tea
Green Tea
Earl Grey

Tea Drinks with Milk:
Chai Latte
Matcha Latte
London Fog

Other Drinks:
Steamer
Hot Chocolate

Modifiers:
Milk options: Whole, 2%, Oat, Almond, 2% Lactose Free; Default option: whole
Espresso shots: Single, Double, Triple, Quadruple; default: Double
Caffeine: Decaf, Regular; default: Regular
Hot-Iced: Hot, Iced; Default: Hot
Sweeteners (option to add one or more): vanilla sweetener, hazelnut sweetener, caramel sauce, chocolate sauce, sugar free vanilla sweetener
Special requests: any reasonable modification that does not involve items not on the menu, for example: 'extra hot', 'one pump', 'half caff', 'extra foam', etc.

"dirty" means add a shot of espresso to a drink that doesn't usually have it, like "Dirty Chai Latte".
"Regular milk" is the same as 'whole milk'.
"Sweetened" means add some regular sugar, not a sweetener.

Soy milk has run out of stock today, so soy is not available.
"""

ordering_system = [add_to_order, get_order, remove_item, clear_order, confirm_order, place_order]

# Toggle this to switch between Gemini 1.5 with a system instruction, or Gemini 1.0 Pro.
use_sys_inst = False

model_name = 'gemini-1.5-flash' if use_sys_inst else 'gemini-1.0-pro'

if use_sys_inst:
  model = genai.GenerativeModel(
      model_name, tools=ordering_system, system_instruction=COFFEE_BOT_PROMPT)
  convo = model.start_chat(enable_automatic_function_calling=True)

else:
  model = genai.GenerativeModel(model_name, tools=ordering_system)
  convo = model.start_chat(
      history=[
          {'role': 'user', 'parts': [COFFEE_BOT_PROMPT]},
          {'role': 'model', 'parts': ['OK I understand. I will do my best!']}
        ],
      enable_automatic_function_calling=True)


@retry.Retry(initial=30)
def send_message(message):
  return convo.send_message(message)


placed_order = []
order = []

print('Welcome to Barista bot!\n\n')

while not placed_order:
  response = send_message(input('> '))
  print(response.text)


print('\n\n')
print('[barista bot session over]')
print()
print('Your order:')
print(f'  {placed_order}\n')
print('- Thanks for using Barista Bot!')