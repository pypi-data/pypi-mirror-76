(一)：安装

-  从 PYPI 安装

::

    pip install -U  feishu-plain-message

-  从 Github 安装

::

    pip install git+https://github.com/yinhuanyi/feishu-plain-message.git


(二)：使用方法

::

    from feishu_message import FeishuPlainMessage

    if __name__ == '__main__':
        feishu = FeishuPlainMessage('13970236750', 'cli_9f9b87ccdsc970d00b', 'SVWv3GtMxkVlPgo0feOsdsUhyA728025qnf')

        feishu.send_message('工单类型+工单ID', '工单基本内容')