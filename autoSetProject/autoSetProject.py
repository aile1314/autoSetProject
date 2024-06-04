import maya.cmds as cmds
import os

def set_project_on_scene_open():
    # 現在のシーンのファイルパスを取得
    scene_path = cmds.file(query=True, sceneName=True)
    
    if scene_path:
        # シーンファイルのディレクトリを取得
        scene_dir = os.path.dirname(scene_path)
        
        # workspace.melのあるディレクトリを見つける
        workspace_mel_dir = find_workspace_mel_dir(scene_dir)
        
        if workspace_mel_dir:
            # workspace.melが見つかったディレクトリをプロジェクトとして設定
            cmds.workspace(workspace_mel_dir, openWorkspace=True)
            print(f"Project set to: {workspace_mel_dir}")
        else:
            print("Workspace.mel not found in parent directories. Project not set.")
    else:
        print("No scene open. Project not set.")

def find_workspace_mel_dir(start_dir):
    # start_dirから上位ディレクトリを再帰的に検索してworkspace.melを見つける
    current_dir = start_dir
    while current_dir:
        workspace_mel_path = os.path.join(current_dir, "workspace.mel")
        if os.path.exists(workspace_mel_path):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            # ルートディレクトリに到達した場合、探索を終了
            break
        current_dir = parent_dir
    return None

# コールバックを登録
callbacks = []

def register_callbacks():
    global callbacks
    callbacks.append(cmds.scriptJob(event=["SceneOpened", set_project_on_scene_open], protected=True))

def unregister_callbacks():
    global callbacks
    for callback in callbacks:
        cmds.scriptJob(kill=callback, force=True)
    callbacks = []

# Mayaの起動時にコールバックを登録
register_callbacks()
