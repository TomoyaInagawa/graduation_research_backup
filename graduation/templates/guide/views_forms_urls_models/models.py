from accounts.models import CustomUser
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


# 利用者
class GeneralUser(models.Model):
    
    customuser = models.OneToOneField(CustomUser, verbose_name='カスタムユーザー', on_delete=models.PROTECT,
        related_name='generaluser')
    post = models.CharField(verbose_name='郵便番号', max_length=7)
    call = models.CharField(verbose_name='電話番号', max_length=21)
    birthday = models.DateField(verbose_name='生年月日')

    class Meta:
        verbose_name_plural = '利用者'
    
    def __str__(self):
        return self.customuser.name



# 管理者
class AdminUser(models.Model):
    
    customuser = models.OneToOneField(CustomUser, verbose_name='カスタムユーザー', on_delete=models.PROTECT,
        related_name='adminuser')
    is_advanced = models.BooleanField(verbose_name='上級フラグ')

    class Meta:
        verbose_name_plural = '管理者'
    
    def __str__(self):
        return self.customuser





# 地区
class District(models.Model):
    
    name = models.CharField(verbose_name='地区名', max_length=100)

    class Meta:
        verbose_name_plural = '地区'
    
    def __str__(self):
        return self.name




# 移動手段
class Transportation(models.Model):
    
    name = models.CharField(verbose_name='名称', max_length=50)

    class Meta:
        verbose_name_plural = '移動手段'
    
    def __str__(self):
        return self.name



# 場所
class Place(models.Model):
    
    id = models.CharField(verbose_name='場所ID', max_length=50, primary_key=True)
    name = models.CharField(verbose_name='名称', max_length=50)
    explanation = models.TextField(verbose_name='説明')
    addDateTime = models.DateTimeField(verbose_name='追加日時', auto_now_add=True)
    updateDateTime = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    placeType = models.CharField(verbose_name='場所タイプ',  max_length=100)
    location = models.CharField(verbose_name='所在地', max_length=100)
    call = models.CharField(verbose_name='電話番号',  max_length=13)
    openingHours = models.TimeField(verbose_name='営業開始時間')
    endingHours = models.TimeField(verbose_name='営業終了時間')
    regularHoliday = models.CharField(verbose_name='定休日', max_length=100)
    url = models.URLField(verbose_name='URL')
    district = models.ForeignKey(District, verbose_name='地区', on_delete=models.PROTECT, related_name='Place')
    furigana = models.CharField(verbose_name='ふりがな', max_length=100)

    class Meta:
        verbose_name_plural = '場所'
    
    def __str__(self):
        return self.name



# 観光地
class TouristArea(models.Model):

    place = models.OneToOneField(Place, verbose_name='場所', on_delete=models.PROTECT,
        related_name='touristArea')
    picture = models.ImageField(verbose_name='写真', )

    class Meta:
        verbose_name_plural = '観光地'
    
    def __str__(self):
        return self.place.name




# ガイドコース
class GuideCourse(models.Model):
    
    id = models.AutoField(verbose_name='ガイドコースID', max_length=12, primary_key=True)
    title = models.CharField(verbose_name='名称', max_length=50)
    explanation = models.TextField(verbose_name='ガイドコース説明')
    author = models.ForeignKey(CustomUser, verbose_name='作成者', on_delete=models.PROTECT)
    addDateTime = models.DateTimeField(verbose_name='追加日時', auto_now_add=True)
    updateDateTime = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    start = models.ForeignKey(Place,verbose_name='スタート地点', on_delete=models.PROTECT)
    picture = models.ImageField(verbose_name='写真',)
    comment = models.TextField(verbose_name='コメント')
    stayTime = models.IntegerField(verbose_name='滞在時間（時）', validators=[MinValueValidator(0)])
    stayMinute = models.IntegerField(verbose_name='滞在時間（分）', validators=[MinValueValidator(0)])

    # 所要時間の合計を計算()
    def getAllTime(self):
        time = 0
        time += self.stayTime*60+self.stayMinute
        for x in self.AddGuideCourse.all():
            time += x.travelTime*60+x.travelMinute
        return time

    class Meta:
        verbose_name_plural = 'ガイドコース'

    def __str__(self):
        return self.title
    



# ガイドコースのお気に入り
class GuideCourseLike(models.Model):
    
    generaluser = models.ForeignKey(GeneralUser, verbose_name='利用者', on_delete=models.PROTECT)
    guideCourse = models.ForeignKey(GuideCourse, verbose_name='お気に入りのガイドコース', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'お気に入りのガイドコース'
    
    def __str__(self):
        return self.guideCourse.title



# 追加のガイドコース
class AddGuideCourse(models.Model):
    
    guidecourse = models.ForeignKey(GuideCourse,verbose_name='ガイドコース', on_delete=models.CASCADE, related_name='AddGuideCourse')
    arrivalPoint = models.ForeignKey(Place,verbose_name='到着地点', on_delete=models.PROTECT, related_name='AddGuideCourse')
    transportation = models.ForeignKey(Transportation,verbose_name='移動手段', on_delete=models.PROTECT, related_name='AddGuideCourse')
    travelTime = models.IntegerField(verbose_name='移動時間（時）')
    travelMinute = models.IntegerField(verbose_name='移動時間（分）')
    picture = models.ImageField(verbose_name='写真', null=True,)
    comment = models.TextField(verbose_name='コメント')
    stayTime = models.IntegerField(verbose_name='滞在時間（時）', validators=[MinValueValidator(0)])
    stayMinute = models.IntegerField(verbose_name='滞在時間（分）', validators=[MinValueValidator(0)])

    class Meta:
        verbose_name_plural = '追加のガイドコース'
    
    def __str__(self):
        return "→"+self.transportation.name+"→"+self.arrivalPoint.name




# 店のカテゴリー
class StoreCategory(models.Model):
    
    name = models.CharField(verbose_name='カテゴリー名', max_length=100)

    class Meta:
        verbose_name_plural = '店のカテゴリー'
    
    def __str__(self):
        return self.name



# 店のサブカテゴリー
class StoreSubCategory(models.Model):
    
    storeCategory = models.ForeignKey(StoreCategory,verbose_name='店のカテゴリー', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = '店のサブカテゴリー'
    
    def __str__(self):
        return self.storeCategory.name



# 店
class Store(models.Model):
    
    place = models.OneToOneField(Place, verbose_name='場所', on_delete=models.PROTECT,
        related_name='shopuser')
    subCategory = models.ForeignKey(StoreSubCategory,verbose_name='店のサブカテゴリー',on_delete=models.PROTECT)
    pic1 = models.ImageField(verbose_name='写真１', )
    pic2 = models.ImageField(verbose_name='写真２', )
    pic3 = models.ImageField(verbose_name='写真３', )
    pic4 = models.ImageField(verbose_name='写真４', )
    pic5 = models.ImageField(verbose_name='写真５', )

    class Meta:
        verbose_name_plural = '店'
    
    def __str__(self):
        return self.place.name



# グルメのカテゴリー
class GourmetCategory(models.Model):
    
    name = models.CharField(verbose_name='カテゴリー名', max_length=50)

    class Meta:
        verbose_name_plural = 'グルメのカテゴリー'
    
    def __str__(self):
        return self.name



# グルメ
class Gourmet(models.Model):
    
    id = models.CharField(verbose_name='グルメID', max_length=12, primary_key=True)
    name = models.CharField(verbose_name='名称', max_length=50)
    explanation = models.TextField(verbose_name='グルメ説明')
    category = models.ForeignKey(GourmetCategory, verbose_name='カテゴリー', on_delete=models.PROTECT)
    addDateTime = models.DateTimeField(verbose_name='追加日時', auto_now_add=True)
    updateDateTime = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    pic1 = models.ImageField(verbose_name='写真１', )
    pic2 = models.ImageField(verbose_name='写真２', )
    pic3 = models.ImageField(verbose_name='写真３', )
    pic4 = models.ImageField(verbose_name='写真４', )
    pic5 = models.ImageField(verbose_name='写真５', )

    class Meta:
        verbose_name_plural = 'グルメ'
    
    def __str__(self):
        return self.name



# 飲食店
class Restaurant(models.Model):
    
    store = models.OneToOneField(Store, verbose_name='店', on_delete=models.PROTECT, related_name='Restaurant')

    class Meta:
        verbose_name_plural = '飲食店'
    
    def __str__(self):
        return self.name


# 店が登録しているグルメ
class StoreGourmet(models.Model):
    
    restaurant = models.ForeignKey(Restaurant, verbose_name='飲食店', on_delete=models.PROTECT)
    gourmet = models.ForeignKey(Gourmet, verbose_name='グルメ', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = '店が登録しているグルメ'
    
    def __str__(self):
        return self.restaurant



# スタンプ
class Stamp(models.Model):
    
    id = models.CharField(verbose_name='スタンプID', max_length=50, primary_key=True)
    name = models.CharField(verbose_name='名称', max_length=50)
    year = models.IntegerField(verbose_name='取得できる年')
    addDateTime = models.DateTimeField(verbose_name='追加日時', auto_now_add=True)
    updateDateTime = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    place = models.ForeignKey(Place, verbose_name='スタンプの場所', on_delete=models.PROTECT)
    pic_big = models.ImageField(verbose_name='写真(大)', )
    pic_small = models.ImageField(verbose_name='写真(小)', )

    class Meta:
        verbose_name_plural = 'スタンプ'
    
    def __str__(self):
        return self.name


# スタンプラリー
class StampRally(models.Model):

    generalUser = models.ForeignKey(GeneralUser, verbose_name='利用者', on_delete=models.PROTECT)
    stamp = models.ForeignKey(Stamp, verbose_name='集めたスタンプ', on_delete=models.PROTECT)
    date = models.DateTimeField(verbose_name='取得した日付', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'スタンプラリー'
    
    def __str__(self):
        return self.generalUser


# 場所のお気に入り
class PlaceLike(models.Model):
    
    generalUser = models.ForeignKey(GeneralUser, verbose_name='利用者', on_delete=models.PROTECT)
    place = models.ForeignKey(Place, verbose_name='お気に入りの場所', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = '場所のお気に入り'
    
    def __str__(self):
        return self.place.name

