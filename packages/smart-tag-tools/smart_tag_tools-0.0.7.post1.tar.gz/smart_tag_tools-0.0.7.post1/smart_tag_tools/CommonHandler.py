#!/usr/bin/python3
# -*- coding:utf-8 -*-


class FieldHandler:
    """
    适用结构：字典列表嵌套结构
    """

    @classmethod
    def update_field_value(cls, val, **fields):
        """
        修改字段值
        :param val:
        :param fields:
        :return:
        """
        if isinstance(val, dict):
            for field, v in fields.items():
                if field in val:
                    val[field] = v

            for key in val:
                cls.update_field_value(val[key], **fields)

        if isinstance(val, list):
            for item in val:
                cls.update_field_value(item, **fields)

    @classmethod
    def update_field_name(cls, val, **fields):
        """
        修改字段名
        :param val:
        :param fields:
        :return:
        """
        if isinstance(val, dict):
            for field, v in fields.items():
                if field in val:
                    val[v] = val.pop(field)

            for key in val:
                cls.update_field_name(val[key], **fields)

        if isinstance(val, list):
            for item in val:
                cls.update_field_name(item, **fields)

    @classmethod
    def remove_field(cls, val, *fields):
        """
        删除字段（递归）
        @param val:
        @param fields:
        @return:
        """
        if isinstance(val, dict):
            for field in fields:
                val.pop(field, "404")

            for key in val:
                cls.remove_field(val[key], *fields)

        if isinstance(val, list):
            for item in val:
                cls.remove_field(item, *fields)

    @classmethod
    def add_field(cls, val, **fields):
        """
        添加字段,只针对列表
        :param val:
        :param fields:
        :return:
        """

        if isinstance(val, list):
            for item in val:
                for field, v in fields.items():
                    item[field] = v
