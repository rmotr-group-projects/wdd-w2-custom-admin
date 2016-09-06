# Custom admin for a blogging platform

The platform is really simple. There are just blogs, authors and entries. An `Entry` is created by an `Author` and exists inside a `blog`. The models are already created for you. Let's start describing the changes to the admin you'll have to do.

## Scoring

Each Entry has a "scoring". You have to build a custom action to reset that score for a set of selected entries:

![image](https://cloud.githubusercontent.com/assets/872296/18292062/b61ad3fc-7461-11e6-9c93-1ff7adf8cc1b.png)

After this action is applied, the score of all the entries should be `0`.

## Moving an entry to a different blog

You need to write other custom action to move an entry to a different blog. This action should have an intermediate step that will let the user select the blog

**Step 1 select the entry to move**
![image](https://cloud.githubusercontent.com/assets/872296/18292135/03e4d704-7462-11e6-8ce5-0df2e94fd570.png)

**Step 2 select the blog to move the entry to**
![image](https://cloud.githubusercontent.com/assets/872296/18292184/461d0d62-7462-11e6-9dc2-f6936a3868db.png)

## Custom login page

Our blogging platform will support login with Github. So we want to make that option available to our users. You'll need to change the Admin login page to include a "Login with Github" link:

![image](https://cloud.githubusercontent.com/assets/872296/18292253/9cfad434-7462-11e6-8975-5cb85bfcf761.png)

**Important** You DON'T need to actually implement the Github login. Just find a way to put the link in the admin login page.

## Custom select2 input in the admin

The Entry add/change view should include [select2](https://select2.github.io/) instead of regular inputs.

![image](https://cloud.githubusercontent.com/assets/872296/18292358/27a282b2-7463-11e6-80b0-5d79dfe08659.png)

Hint: [This](http://django-easy-select2.readthedocs.io/en/latest/) might be useful ;)

## Custom admin view (and URL)

You'll need to write a custom view to display some stats about the blogging platform. To do that, the easiest way is to create a custom view for the admin. In order to do that, the [get_urls](https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_urls) method from the ModelAdmin might be handy.

![image](https://cloud.githubusercontent.com/assets/872296/18291867/d3b7ce98-7460-11e6-9dff-a3a5f07bb0fa.png)
