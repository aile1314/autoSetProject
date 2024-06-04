# autoSetProject
Autodesk Mayaでシーンファイルを開いたとき、自動でプロジェクトセットとオートセーブの保存先を設定するpythonのプログラムです。

# 《導入方法》
Maya2023で起動確認しました。
「autoSetProject」フォルダーと「userSetup.py」ファイルをドキュメントにあるMayaのスクリプトファイルに設置するだけです。

すでに「userSetup.py」ファイルがあるならそこに「from autoSetProject import autoSetProject」と「from autoSetProject import autosave」を追加すれば使えるようになります。

# <実装機能>
・Mayaのファイルを開いた際にそのファイルがあるプロジェクトを見つけ、セットします。

・セットしたプロジェクトの「autosave」フォルダーに開いたファイルと同名のフォルダーを作成し、10分ごとに作業しているファイルを保存します。

# ＜変更点（2024/06/04）＞
・一つになっていたファイルをセットプロジェクト用とアートセーブ用に変更

・オートセーブ機能はMaya標準のものを使用
