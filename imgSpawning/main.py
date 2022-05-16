from fastapi import FastAPI
from random import randint
from PIL import Image, ImageDraw
from aleph_client.asynchronous import get_posts, create_store, get_messages
from aleph_client.chains.ethereum import ETHAccount

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/nfts/{id}.json")
async def generateNFT(id: int):
    redValue = randint(0, 255) 
    greenValue = randint(0, 255) 
    blueValue = randint(0, 255) 

    img = Image.new(mode="RGB", size=(400, 400), color=(redValue, greenValue, blueValue))
    
    imgValueInt = int(randint(1, 99999999))
    imgValue = str("Value: ") + str(imgValueInt)
    imageDraw = ImageDraw.Draw(img)
    imageDraw.text((200, 200), imgValue, fill=(255, 255, 255))
    
    img.save("nft.png", format="PNG")

    account = ETHAccount("")
    address = account.get_address()

    response = await get_messages(
        addresses = [address],
        refs = [f'pictureSquare-{id}'],
        message_type = "STORE"
    )

    if len(response["messages"]) > 0:
        hash = response["messages"][0]
    else:
        file = open("./nft.png", "rb").read()
        hash = await create_store(
            file_content=file,
            account=account,
            storage_engine = "ipfs",
            extra_fields = {
                "name": f'Picture Square #{id}',
                "description": f'There is no way that this (pictureSquare-{id}) actually gets sold, right?'
            },
            ref = f'pictureSquare-{id}'
        )

    return {
        "image": f'https://ipfs.io/ipfs/{hash["content"]["item_hash"]}',
        "name": hash["content"]["name"],
        "description": hash["content"]["description"],
    }