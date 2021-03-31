import json
import pyBrickset

client = pyBrickset.Client('4-e3wM-sWsw-Su3pI')
client.login('testuser@test.com', 'P@ssw0rd!')

# themes = client.getThemes()
# top5Themes = themes[:5]
# print(json.dumps(top5Themes, indent=4))

# instructions = client.getInstructions('6905')
# print(json.dumps(instructions, indent=4))

# minifigsOwned = client.getMinifigCollectionOwned()
# top5MinifigsOwned = minifigsOwned[:5]
# print(json.dumps(top5MinifigsOwned, indent=4))

sets = client.getSets(theme='Indiana Jones')
print(json.dumps(sets, indent=4))

# top2Sets = sets[:5]
# print(json.dumps(top2Sets, indent=4))

# sets = client.getSets(owned=1)

# print(json.dumps(sets, indent=4))

# additionalImages = client.getAdditionalImages(setId='6905')
# print(json.dumps(additionalImages, indent=4))

# reviews = client.getReviews(setId='6905')
# print(json.dumps(reviews, indent=4))

# subThemes = client.getSubthemes(Theme='Indiana Jones')
# print(json.dumps(subThemes, indent=4))

# years = client.getYears(Theme='Indiana Jones')
# print(json.dumps(years, indent=4))

# response = client.setCollection(setId=8469, own=1, qtyOwned=5)
# print(json.dumps(response, indent=4))

# userNotes = client.getUserNotes()
# print(json.dumps(userNotes, indent=4))

# minifigsOwned = client.getMinifigCollection(owned=1)
# top5MinifigsOwned = minifigsOwned[:5]
# print(json.dumps(top5MinifigsOwned, indent=4))

# response = client.setMinifigCollection(minifigNumber='colhp28', own=1)
# print(json.dumps(response, indent=4))

# userMinifigNotes = client.getUserMinifigNotes()
# print(json.dumps(userMinifigNotes, indent=4))
