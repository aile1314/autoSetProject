import os
import maya.cmds as cmds
import maya.mel as mel

def set_autosave_directory():
    # 現在のシーンファイルのパスを取得
    scene_path = cmds.file(query=True, sceneName=True)
    
    if not scene_path:
        print("シーンファイルが開かれていません。")
        return
    
    # シーンファイル名とプロジェクトディレクトリを取得
    scene_name = os.path.basename(scene_path)
    scene_name_no_ext = os.path.splitext(scene_name)[0]  # 拡張子を除去
    project_dir = cmds.workspace(query=True, rootDirectory=True)
    
    # オートセーブディレクトリのパスを作成
    autosave_dir = os.path.join(project_dir, "autosave", scene_name_no_ext)
    
    # ディレクトリが存在しない場合は作成
    if not os.path.exists(autosave_dir):
        os.makedirs(autosave_dir)
    
    # オートセーブの設定を更新
    cmds.autoSave(en=True)  # オートセーブを有効化
    cmds.autoSave(dst=1)
    #cmds.autoSave(saveInBackground=True)  # バックグラウンドで保存を有効化
    cmds.autoSave(fol=autosave_dir)  # オートセーブのディレクトリを設定
    #cmds.autoSave(maxBackups=10)  # バックアップの最大数を設定（例: 10）
    cmds.autoSave(int=600)  # オートセーブの間隔を設定（例: 10分）
    cmds.autoSave(p=True)

    print("オートセーブディレクトリを設定しました: {}".format(autosave_dir))

# ファイルが開かれたときにスクリプトを実行
callbacks = []

def on_scene_opened(*args):
    set_autosave_directory()

callbacks.append(cmds.scriptJob(event=["SceneOpened", on_scene_opened]))

# Mayaを閉じるときにscriptJobを削除
def remove_callbacks(*args):
    for callback in callbacks:
        if cmds.scriptJob(exists=callback):
            cmds.scriptJob(kill=callback, force=True)

callbacks.append(cmds.scriptJob(event=["quitApplication", remove_callbacks]))
