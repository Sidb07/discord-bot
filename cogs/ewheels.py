import discord
import requests
import random
import json
import os
from bs4 import BeautifulSoup
from discord.ext import commands


class ewheels(commands.Cog):

    def __init__(self, client):
        self.client = client

    os.chdir(r'/home/siddbawane/Desktop/bot')



    @commands.command()
    async def new(self, ctx):
        '''Shows new blog on ewheels'''
        with open('blogs.json', 'r') as f:
            blogs = json.load(f)
                
        url1 = ['https://www.ewheelsindia.com/search?&max-results=10', 'https://www.ewheelsindia.com/search/label/Electric%20Scooters%20&%20Bikes?&max-results=10', 'https://www.ewheelsindia.com/search/label/Luxury%20Brands?&max-results=10', 'https://www.ewheelsindia.com/search/label/electric%20suv%20and%20trucks?&max-results=10', 'https://www.ewheelsindia.com/search/label/All%20about%20tesla?&max-results=10', 'https://www.ewheelsindia.com/search/label/Electric%20Cars?&max-results=10', 'https://www.ewheelsindia.com/search/label/indian%20startups%20and%20brands?&max-results=10']
        repeating = ['https://www.ewheelsindia.com/p/advertise-here.html', 'https://www.ewheelsindia.com/p/privacy-policy.html', 'https://www.ewheelsindia.com/p/about-us_9.html' ]
            
        flag = 0
        for url in url1:
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text)
        
            for link in soup.findAll('a'):
                href = str(link.get('href'))
                if href.endswith('.html') and href not in repeating and href not in blogs:
                    blogs.append(href)
                    flag=1;
                    gg = discord.Embed(title = "NEW BLOG:", description="New blog uploaded on ewheels go check it out", colour= 0xFF9384)
                    gg.add_field(name="Link:", value=href, inline=False)
                    gg.set_thumbnail(url = "https://1.bp.blogspot.com/-SUNyALCai0M/XWtPQZ6EY7I/AAAAAAAAQfQ/AGowsRX5jl4ZyxwMD5EwZ70iRIP6RS1LgCLcBGAs/s320/IMG_20181111_113621.jpg")
                    gg.set_image(url = "https://1.bp.blogspot.com/-M_KIswP7-hQ/XregAykQF-I/AAAAAAAAAGQ/z4tacp9AIuoBbi5YkW5DbPEN7kRHBa1GgCK4BGAYYCw/s1600/logo%2Bbanner%2B%25281%2529.png")
                    await ctx.send(embed= gg)

        if flag is 0:
            em = discord.Embed(colour = 0xFF7323)
            em.add_field(name = "Not Found", value="Currently there are no new blogs type (.blog) for a random blog on ewheels", inline=False)
            await ctx.send(embed = em)
        
        with open('blogs.json', 'w') as f:
            json.dump(blogs, f)

    @commands.command()
    async def blog(self, ctx):
        '''shows a random blog on ewheels'''
        with open('blogs.json', 'r') as f:
            blogs = json.load(f)

        blg = discord.Embed(title = "BLOG", description="Here's a random blog on ewheels", colour= 0xFF9823)
        ans = random.choice(blogs)
        blg.add_field(name="Link:", value=ans, inline=False)
        blg.set_thumbnail(url = "https://1.bp.blogspot.com/-SUNyALCai0M/XWtPQZ6EY7I/AAAAAAAAQfQ/AGowsRX5jl4ZyxwMD5EwZ70iRIP6RS1LgCLcBGAs/s320/IMG_20181111_113621.jpg")
        blg.set_image(url = "https://1.bp.blogspot.com/-M_KIswP7-hQ/XregAykQF-I/AAAAAAAAAGQ/z4tacp9AIuoBbi5YkW5DbPEN7kRHBa1GgCK4BGAYYCw/s1600/logo%2Bbanner%2B%25281%2529.png")
        await ctx.send(embed = blg)   

        with open('blogs.json', 'w') as f:
            json.dump(blogs, f) 

    @commands.command()
    async def number(self, ctx):
        with open('blogs.json', 'r') as f:
            blogs = json.load(f)

        no = len(blogs)
        await ctx.send(f'There are {no} blogs on ewheels so far')

        with open('blogs.json', 'w') as f:
            json.dump(blogs, f) 
       

def setup(client):
    client.add_cog(ewheels(client))