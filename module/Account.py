#!/usr/bin/env python
# coding=utf-8
#
# import sys
# sys.path.append("../../../")

import hashlib
import time
import logging
from module.DB import db
from module.util.convert import convert
from module.Error import LoginError
from module.define import *
from module.Favourite import Favourite


LEVELS = {
    'debug':logging.DEBUG,
    'info':logging.INFO,
    'warning':logging.WARNING,
    'error':logging.ERROR,
    'critical':logging.CRITICAL
}

ACCOUNT_USER = 'account:{uid}' # hash
ACCOUNT_FAVOURITE='account:{uid}:favourite' #set，存放用户所拥有的收藏夹的id
ADMIN = 'admin' # set
ACCOUNT_EMAIL = 'account:email:{email}' # String
ACCOUNT_LOGIN = 'account:login:set' # zset key=uid, value=login time
SESSION_USER = 'session:{uid}' # String
ACCOUNT_COUNT = 'account:count' # String
NICKNAME = 'nickname' # set 存所有nickname， 查重用
EMAIL = 'email' # set 存所有email，查重用
ACCOUNT_USERLIST = 'account:userlist' # set
ACCOUNT_LINK = 'account:{uid}:link' #Set
ACCOUNT_AVATARS = 'account:{uid}:avatars'


class Account(object):
    db = db
    userinfo = {}




    def __init__(self, uid=0):
        uid = int(uid)

        if not isinstance(uid, int):
           raise TypeError('Bad operand type')

        self.db = db
        self.uid = uid
        self.key = ACCOUNT_USER.format(uid=uid)
        self.account_key = ACCOUNT_USER.format(uid=uid)

    def favourites(self):
        """
        返回用户所有的收藏夹，
        返回列表，其中包含收藏夹对象
        """
        account_favourite = ACCOUNT_FAVOURITE.format(uid=self.uid)

        tmp = self.db.smembers(account_favourite)
        result = []

        for k in tmp:
            result.append(Favourite(k))

        return result

    def add_favourite(self, fid):
        """
        添加收藏夹id到用户收藏夹表中

        操作表：
        account:{id}:favourite|(set)
        """
        account_favourite = ACCOUNT_FAVOURITE.format(uid=self.uid)
        self.db.r.sadd(account_favourite, fid)

    def _get(self, field, default=None):
        """
        field:
            查询的key
        default:
            值不存在时返回的默认值

        内部函数，返回用户中指定的信息
        支持nickname, email, mobile, age, sex, password, desc, status, avatar

        返回值：
            成功,返回相应数据
            失败,返回{default}
        """
        # result = self.db.hget(self.account_key, field)
        # return result

        if field in self.userinfo:
            return self.userinfo[field]
        else:
            result = self.db.hget(self.account_key, field)
            return result if result else default

        # if result:
        #     return result
        # else:
        #     return None

    def _set(self, field, value):
        """
        内部函数，设置用户指定的数据，
        若要保存到数据库，还需调用save()方法
        """
        return self.db.hset(self.key, field, value)

    @property
    def email(self):
        return self._get('email')

    @property
    def mobile(self):
        return self._get('mobile')

    @property
    def age(self):
        return self._get('age', 0)

    @property
    def sex(self):
        return self._get('sex')
        # if 'sex' in self.userinfo:
        #     return self.userinfo['sex']
        # else:
        #     sex = self._get('sex')
        #     return sex if sex else ''

    @property
    def nickname(self):
        """
        返回用户的昵称
        先检查用户的key是否被修改过
        若修改过，返回修改过的值，否则从数据库中取出
        """
        # key = 'nickname'
        return self._get('nickname')

    @nickname.setter
    def nickname(self, value):
        self.userinfo['nickname'] = value
        return self.nickname

    @property
    def password(self):
        return self._get('password')

    @property
    def desc(self):
        return self._get('desc')

    @property
    def status(self):
        return self._get('status')

    @property
    def expired(self):
        """
        获取cookie 过期时间，若数据库中无数据，则默认为3600秒
        """
        time = self._get('expired')
        if time:
            return int(time)
        else:
            return 3600

    def isAdmin(self):
        """
        检查用户是否是管理员

        暂时设置id 为1的是管理员
        这个验证功能应该拆分到auth类中，不过以后有空重构的时候再说吧
        """
        # test admin data start
        self.db.r.sadd(ADMIN, 1)
        # test admin data end

        if self.db.r.sismember(ADMIN, self.uid):
            return True
        else:
            return False

    @classmethod
    def login(cls, email, password):
        """
        登陆功能
        为了代码不那么散，我就把登陆注册等与具体Account类无关联的操作放在了Account中，也不知道这样做好不好。。。
        """
        # account = Account()
        email = email
        password = password

        if email is None:
            raise LoginError("email is None!")
        if password is None:
            raise LoginError("password is None!")

        account_email = ACCOUNT_EMAIL.format(email=email)
        if cls.db.r.exists(account_email) is False:
            raise LoginError("Email does not exists!")

        uid = int(cls.db.get(account_email))
        account_user = ACCOUNT_USER.format(uid=uid)
        if cls.db.hget(account_user, 'password') != password:
            raise LoginError("Incorrect passord!")

        account_login = ACCOUNT_LOGIN
        session = SESSION_USER.format(uid=uid)
        lastlogin = dict(
            ip="127.0.0.1",
            time =int(time.time())
        )

        cls.db.r.zadd(account_login, uid, 1)
        # session setting
        cls.db.set(session, uid, Account(uid).expired)

        return uid

    @classmethod
    def register(cls, userinfo):
        """
        用户注册，userinfo是dict类型，存储用户的所有信息

        成功返回用户uid，失败返回0
        """
        account_email = ACCOUNT_EMAIL.format(email=userinfo.get('email'))
        account_count = ACCOUNT_COUNT
        nickname_set = NICKNAME
        email_set = EMAIL
        uid = 0

        if cls.db.r.exists(account_email) is True:
            raise LoginError("email is exists!")

        uid = cls.db.r.incr(account_count)

        account_userlist = ACCOUNT_USERLIST
        account_user = ACCOUNT_USER.format(uid=uid)

        cls.db.r.set(account_email, uid)
        cls.db.r.sadd(account_userlist, uid)
        cls.db.r.hmset(account_user, userinfo)
        cls.db.r.sadd(nickname_set, userinfo.get('nickname'))
        cls.db.r.sadd(email_set, userinfo.get('email'))

        return uid

    @classmethod
    def isLogin(cls, uid=0):
        """
        用户是否登陆
        account:login:set (zset)
        check session:{id}
        """
        session_user = SESSION_USER.format(uid=uid)
        if cls.db.r.exists(session_user):
            return True
        else:
            return False

    def logout(self):
        """
        用户退出
        """
        account_login = ACCOUNT_LOGIN
        session_user = SESSION_USER.format(uid=self.uid)

        try:
            self.db.r.zrem(account_login, self.uid)
            self.db.r.delete(session_user)
            return True
        except:
            return False

    def links(self):
        """
        用户发布的所有链接

        成功返回列表，内含Link实例，失败返回空列表
        """
        result = self.db.r.smembers(ACCOUNT_LINK.format(uid=self.uid))
        result = list(result)
        links = []
        for k in result:
            from module import Link
            # links.append(convert(self.db.r.hgetall(LINK.format(lid=bytes.decode(k)))))
            links.append(Link(k))

        return links

    def avatars(self, value=None):
        key = ACCOUNT_AVATARS.format(id=self.id)

        if value is None:
            return self.db.r.smembers(key)
        else:
            return self.db.r.sadd(key, value)

    def update(self, data):
        """
        将修改后的数据写入数据库
        与save方法的区别是update只写入被修改的数据
        """
        account_user = ACCOUNT_USER.format(uid=self.uid)
        user = {
            'uid':self.uid,
            'email':self.email,
            'nickname':self.nickname,
            'password':self.password,
            'sex':self.sex,
            'age':self.age,
            'desc':self.desc,
            'status':self.status,
            'mobile':self.mobile,
            'expired':self.expired,
        }
        # 字典推导式,取出data 与 user 的交集,并生成新字典
        info = {key:data[key] for key in data.keys() & user.keys()}
        print(info)
        result = self.db.r.hmset(account_user, info)
        return result

    def save(self):
        """
        将当前的用户类所有信息写入数据库中
        先从类中提取所有信息，组合数据，然后依次写入数据库
        保存所有数据
        """
        user = {
            'uid':self.uid,
            'email':self.email,
            'nickname':self.nickname,
            'password':self.password,
            'sex':self.sex,
            'age':self.age,
            'desc':self.desc,
            'status':self.status,
            'mobile':self.mobile,
            'expired':self.expired,
        }
        if user['uid'] == 0: raise TypeError("uid 不能为0")

        account_email = ACCOUNT_EMAIL.format(email=userinfo['email'])
        nickname_set = NICKNAME
        email_set = EMAIL
        if self.db.r.exists(account_email) is True:
            print(user)
        # account_email = ACCOUNT_EMAIL.format(email=userinfo.get('email'))
        # account_count = ACCOUNT_COUNT
        # nickname_set = NICKNAME
        # email_set = EMAIL
        # uid = 0
        #
        # if cls.db.r.exists(account_email) is True:
        #     raise LoginError("email is exists!")
        #
        # uid = cls.db.r.incr(account_count)
        #
        # account_userlist = ACCOUNT_USERLIST
        # account_user = ACCOUNT_USER.format(uid=uid)
        #
        # cls.db.r.set(account_email, uid)
        # cls.db.r.sadd(account_userlist, uid)
        # cls.db.r.hmset(account_user, userinfo)
        # cls.db.r.sadd(nickname_set, userinfo.get('nickname'))
        # cls.db.r.sadd(email_set, userinfo.get('email'))
        # return self.userinfo

if __name__ == '__main__':
    from DB import db
    user = Account()
    user.nickname = 10;
    user.save()
