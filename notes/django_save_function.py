def save_function(article_list):
    """Save articles to the database.
    Saves articles to the database if they do not already exist.
    Parameters:
        article_list (json, str): A JSON list of article objects.
    Returns:
        News (class News): Article objects for each unique article.
    """
    source = article_list[0]['source']
    new_count = 0

    error = True
    try:
        latest_article = News.objects.filter(source=source).order_by('-id')[0]
        print(latest_article.published)
        print('var TestTest: ', latest_article, 'type: ', type(latest_article))
    except Exception as e:
        print('Exception at latest_article: ')
        print(e)
        error = False
        pass
    finally:
        # if the latest_article has an index out of range (nothing in model) it will fail
        # this catches failure so it passes the first if statement        
        if error is not True:
            latest_article = None

    for article in article_list:
        # latest_article is None signifies empty DB
        if latest_article is None:
            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except Exception as e:
                print('failed at latest_article is none')
                print(e)
                break
        
        # latest_article.published date < article['published']
        # halts the save, to avoid repetitive DB calls on already existing articles
        elif latest_article.published < article['published']:
            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except:
                print('failed at latest_article.published < j[published]')
                break
        else:
            return print('news scraping failed')

    logger.info(f'New articles: {new_count} articles(s) added.')
    return print('finished')