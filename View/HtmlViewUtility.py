class HtmlViewUtility:
    def getImagePage(self, image):
        return '''<html>
<body>
    <image src="file:///''' + image + '''" width="100%" height="100%" />
</body>
</html>
'''
